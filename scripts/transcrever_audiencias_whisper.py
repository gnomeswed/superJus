#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MÓDULO DE TRANSCRIÇÃO E AUDITORIA DE AUDIÊNCIAS E INTERCEPTAÇÕES TELEFÔNICAS — SUPERJUS
======================================================================================
Processamento forense de áudios e vídeos de audiências (AIJ, Tribunal do Júri, Teams,
PJe Mídias) e interceptações telefônicas (WhatsApp, escutas policiais e gravações ambientais).

Recursos de Alta Performance:
  - Motor Whisper de alta performance (faster-whisper via CTranslate2 com fallback para openai-whisper)
  - Timestamps detalhados por segmento e palavra (word-level timestamps)
  - Divisão inteligente de oradores por análise de pausas acústicas, pontuações e turnos dialógicos
  - Fusão sequencial de falas contíguas do mesmo orador
  - Auditoria penal automática de termos-chave ("droga", "arma", "furto", "flagrante", "confissão", "hierarquia", etc.)
  - Gerador de citações jurídicas formatadas prontas para peças (HC, Memoriais, Resposta à Acusação, Apelação)
  - Suporte a múltiplos modos: audiência (AIJ), interceptação telefônica, tribunal do júri e reuniões Teams
  - Offset temporal configurável para trechos fatiados de mídias longas
  - Exportação multi-formato: TXT, MD, SRT, JSON, Dossiê de Auditoria e Citações Jurídicas
  - Integração nativa com a Memória Persistente memU

Autor: Analista Jurídico Criminal de Alta Performance — SuperJus
"""

import os
import sys
import re
import json
import time
import shutil
import argparse
import tempfile
import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

# Força codificação UTF-8 padrão no terminal Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# ==============================================================================
# DICIONÁRIO DE TERMOS-CHAVE CRIMINAIS PARA AUDITORIA FORENSE
# ==============================================================================
DEFAULT_CRIMINAL_KEYWORDS = {
    "Drogas & Tráfico (Lei 11.343/06)": [
        "droga", "drogas", "entorpecente", "entorpecentes", "maconha", "cocaína",
        "crack", "haxixe", "sintética", "ecstasy", "tráfico", "traficante",
        "artigo 33", "art. 33", "endolação", "balança", "trouxinha", "pino",
        "tablete", "quilo", "gramas", "venda de drogas", "boca de fumo"
    ],
    "Associação & Facção Criminosa": [
        "facção", "facção criminosa", "comando vermelho", "cv", "pcc", "tcp",
        "ada", "amigos dos amigos", "hierarquia", "chefe", "liderança",
        "subordinação", "divisão de tarefas", "estabilidade", "permanência",
        "artigo 35", "art. 35", "associação", "organização criminosa"
    ],
    "Armas & Munições (Estatuto do Desarmamento)": [
        "arma", "armas", "armamento", "fogo", "munição", "munições", "calibre",
        "pistola", "revólver", "fuzil", "porte de arma", "posse de arma",
        "disparo", "confronto", "tiro"
    ],
    "Crimes Patrimoniais (Furto / Roubo)": [
        "furto", "furtos", "roubo", "roubos", "subtração", "subtrair",
        "arrombamento", "concurso de pessoas", "destreza", "receptação"
    ],
    "Prisão, Flagrante & Cautelares": [
        "flagrante", "prisão em flagrante", "mandado de prisão", "preventiva",
        "cautelar", "audiência de custódia", "relaxamento", "conversão",
        "fiança", "liberdade provisória", "art. 312", "artigo 312"
    ],
    "Confissão, Dolo & Declarações": [
        "confissão", "confessou", "admitiu", "declarou", "informou",
        "negou", "dolo", "intenção", "espontânea", "coação"
    ],
    "Materialidade, Apreensão & Cadeia de Custódia": [
        "apreensão", "apreendido", "apreendida", "materialidade", "laudo",
        "perícia", "pericial", "laudo toxicológico", "confronto vocálico",
        "cadeia de custódia", "lacre", "acondicionamento", "inviolabilidade",
        "espelhamento", "hash"
    ],
    "Nulidades & Garantias Constitucionais": [
        "reconhecimento", "artigo 226", "art. 226", "álbum de fotos",
        "fotográfico", "inépcia", "ilicitude", "tortura", "agressão",
        "excesso de prazo", "isonomia", "artigo 580", "art. 580", "desmembramento"
    ]
}


# ==============================================================================
# FUNÇÕES UTILITÁRIAS DE TEMPO E FORMATAÇÃO
# ==============================================================================
def format_timestamp(seconds: float, include_millis: bool = False) -> str:
    """Converte segundos para o formato [HH:MM:SS] ou [HH:MM:SS,mmm]."""
    if seconds < 0:
        seconds = 0.0
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    millis = int((seconds - int(seconds)) * 1000)

    if include_millis:
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


# ==============================================================================
# GERENCIAMENTO DE MÍDIA (FFMPEG)
# ==============================================================================
class MediaManager:
    """Gerencia conversão, extração e normalização de áudio/vídeo."""

    AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".ogg", ".opus", ".flac", ".aac", ".wma"}
    VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}

    @classmethod
    def is_video(cls, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in cls.VIDEO_EXTENSIONS

    @classmethod
    def is_audio(cls, file_path: str) -> bool:
        ext = os.path.splitext(file_path)[1].lower()
        return ext in cls.AUDIO_EXTENSIONS

    @classmethod
    def check_ffmpeg(cls) -> bool:
        return shutil.which("ffmpeg") is not None

    @classmethod
    def extract_audio_if_needed(cls, media_path: str) -> Tuple[str, bool]:
        """Se o arquivo for vídeo ou formato exótico, extrai áudio mono 16kHz via ffmpeg.
        Retorna (audio_path, is_temporary)."""
        if not os.path.exists(media_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {media_path}")

        ext = os.path.splitext(media_path)[1].lower()
        if ext in cls.AUDIO_EXTENSIONS and ext in {".mp3", ".wav"}:
            return media_path, False

        if not cls.check_ffmpeg():
            print("[!] FFmpeg não detectado no PATH. Tentando processamento direto...")
            return media_path, False

        print(f"[*] Extraindo/normalizando áudio com FFmpeg: {os.path.basename(media_path)}")
        temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()

        cmd = [
            "ffmpeg", "-y", "-i", media_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            temp_wav_path
        ]
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            if os.path.exists(temp_wav_path):
                os.unlink(temp_wav_path)
            print("[!] Falha na extração com ffmpeg. Tentando arquivo original.")
            return media_path, False

        return temp_wav_path, True


# ==============================================================================
# MOTOR WHISPER (FASTER-WHISPER / OPENAI-WHISPER)
# ==============================================================================
class WhisperEngine:
    """Carrega e executa a transcrição forense com timestamps e palavras."""

    def __init__(self, model_name: str = "base", device: str = "auto", compute_type: str = "auto"):
        self.model_name = model_name
        self.device = device
        self.compute_type = compute_type
        self.engine_type = "faster-whisper"
        self.model = None
        self._initialize_engine()

    def _initialize_engine(self):
        resolved_device = "cpu"
        resolved_compute = "int8"

        if self.device == "cuda":
            resolved_device = "cuda"
            resolved_compute = "float16" if self.compute_type == "auto" else self.compute_type
        elif self.device == "cpu":
            resolved_device = "cpu"
            resolved_compute = "int8" if self.compute_type == "auto" else self.compute_type
        else:
            try:
                import torch
                if torch.cuda.is_available():
                    resolved_device = "cuda"
                    resolved_compute = "float16"
            except Exception:
                resolved_device = "cpu"
                resolved_compute = "int8"

        try:
            from faster_whisper import WhisperModel
            print(f"[*] Carregando faster-whisper (modelo: '{self.model_name}', device: {resolved_device}, compute: {resolved_compute})...")
            self.model = WhisperModel(self.model_name, device=resolved_device, compute_type=resolved_compute)
            self.engine_type = "faster-whisper"
            print("[+] Motor faster-whisper carregado com sucesso!")
        except Exception as e:
            print(f"[!] faster-whisper indisponível ou erro ({e}). Tentando fallback para openai-whisper...")
            try:
                import whisper
                self.model = whisper.load_model(self.model_name)
                self.engine_type = "openai-whisper"
                print("[+] Motor openai-whisper carregado com sucesso!")
            except Exception as e2:
                raise RuntimeError(
                    f"Nenhum motor Whisper disponível. Instale faster-whisper ou openai-whisper via pip:\n"
                    f"pip install faster-whisper\nErro original: {e}\nErro fallback: {e2}"
                )

    def transcribe(
        self,
        audio_path: str,
        language: str = "pt",
        beam_size: int = 5,
        word_timestamps: bool = True,
        initial_prompt: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        if initial_prompt is None:
            initial_prompt = (
                "Audiência de Instrução e Julgamento criminal, interceptação telefônica e escuta judicial. "
                "Termos forenses: réu, corréu, denúncia, flagrante, tráfico, associação, art. 33, art. 35, "
                "apreensão, maconha, cocaína, delegacia, delegado, policial militar, depoimento, testemunha, "
                "facção criminosa, inquérito, mandado de busca, laudo pericial, cadeia de custódia."
            )

        print(f"[*] Transcrevendo áudio com Whisper ({self.engine_type})...")
        start_time = time.time()
        segments_list = []
        metadata = {
            "engine": self.engine_type,
            "model": self.model_name,
            "language": language,
            "created_at": datetime.now().isoformat(),
        }

        if self.engine_type == "faster-whisper":
            segments_gen, info = self.model.transcribe(
                audio_path,
                language=language,
                beam_size=beam_size,
                word_timestamps=word_timestamps,
                initial_prompt=initial_prompt,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=400)
            )
            metadata["detected_language"] = info.language
            metadata["language_probability"] = round(info.language_probability, 4)
            metadata["duration_seconds"] = round(info.duration, 2)

            for seg in segments_gen:
                seg_dict = {
                    "id": seg.id,
                    "start": round(seg.start, 3),
                    "end": round(seg.end, 3),
                    "text": seg.text.strip(),
                    "avg_logprob": round(seg.avg_logprob, 3),
                    "no_speech_prob": round(seg.no_speech_prob, 3)
                }
                if word_timestamps and seg.words:
                    seg_dict["words"] = [
                        {
                            "word": w.word.strip(),
                            "start": round(w.start, 3),
                            "end": round(w.end, 3),
                            "probability": round(w.probability, 3)
                        }
                        for w in seg.words
                    ]
                segments_list.append(seg_dict)

        else:
            result = self.model.transcribe(
                audio_path,
                language=language,
                initial_prompt=initial_prompt,
                verbose=False
            )
            metadata["detected_language"] = result.get("language", language)
            for idx, seg in enumerate(result.get("segments", [])):
                segments_list.append({
                    "id": idx,
                    "start": round(seg["start"], 3),
                    "end": round(seg["end"], 3),
                    "text": seg["text"].strip(),
                })

        elapsed = time.time() - start_time
        metadata["transcription_time_seconds"] = round(elapsed, 2)
        print(f"[+] Transcrição concluída em {elapsed:.2f}s ({len(segments_list)} segmentos brutos gerados).")

        return segments_list, metadata


# ==============================================================================
# DIVISÃO DE TURNOS DIALÓGICOS E DIARIZAÇÃO FORENSE
# ==============================================================================
class TurnRefiner:
    """Refina segmentos brutos dividindo perguntas e respostas agrupadas e unindo falas contíguas."""

    @staticmethod
    def split_on_dialog_turns(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Divide segmentos quando detecta '?' ou quebra de turno com pausa significativa."""
        refined = []
        for seg in segments:
            words = seg.get("words", [])
            if not words or len(words) <= 2:
                refined.append(seg)
                continue

            split_indices = []
            for i in range(len(words) - 1):
                w_curr = words[i]
                w_next = words[i + 1]
                word_clean = w_curr["word"].strip()

                # Caso 1: palavra termina com ponto de interrogação '?'
                if word_clean.endswith("?"):
                    split_indices.append(i)
                # Caso 2: pausa considerável entre palavras (>0.8s) com pontuação final
                elif word_clean.endswith((".", "!", ":")) and (w_next["start"] - w_curr["end"] >= 0.7):
                    split_indices.append(i)

            if not split_indices:
                refined.append(seg)
                continue

            # Realiza a divisão dos sub-segmentos
            start_idx = 0
            for idx in split_indices:
                sub_slice = words[start_idx:idx + 1]
                if sub_slice:
                    sub_text = " ".join(w["word"] for w in sub_slice).strip()
                    refined.append({
                        "id": len(refined) + 1,
                        "start": sub_slice[0]["start"],
                        "end": sub_slice[-1]["end"],
                        "text": sub_text,
                        "words": sub_slice,
                        "avg_logprob": seg.get("avg_logprob", 0.0),
                        "no_speech_prob": seg.get("no_speech_prob", 0.0)
                    })
                start_idx = idx + 1

            if start_idx < len(words):
                sub_slice = words[start_idx:]
                sub_text = " ".join(w["word"] for w in sub_slice).strip()
                refined.append({
                    "id": len(refined) + 1,
                    "start": sub_slice[0]["start"],
                    "end": sub_slice[-1]["end"],
                    "text": sub_text,
                    "words": sub_slice,
                    "avg_logprob": seg.get("avg_logprob", 0.0),
                    "no_speech_prob": seg.get("no_speech_prob", 0.0)
                })

        return refined


class SpeakerDiarizer:
    """Classifica e segmenta oradores baseado em modo, pausas, marcadores discursivos e contexto."""

    ROLE_PATTERNS = {
        "Magistrado(a)": [
            r"boa tarde a todos", r"boa noite a todos", r"está presente", r"declaração por todas as defesas",
            r"vamos colher a prova", r"está sob compromisso de dizer a verdade", r"pena de responder criminalmente",
            r"falso-testemunho", r"tenho dever de adverti-lo", r"quem vai indagar primeiramente",
            r"passo a palavra", r"com a palavra", r"pode indagar", r"alguma pergunta complementar",
            r"audiência encerrada", r"termo de audiência", r"vou dar a palavra", r"o senhor é agente público"
        ],
        "Promotor(a) de Justiça": [
            r"boa tarde, doutor", r"boa tarde, senhor", r"pelo ministério público",
            r"o ministério público pergunta", r"como começou a operação", r"como começaram as investigações",
            r"o senhor participou da diligência", r"constatou a apreensão", r"sem mais perguntas pelo mp",
            r"o mp insiste", r"satisfeito, excelência", r"obrigada, excelência", r"obrigado, excelência"
        ],
        "Advogado(a) de Defesa": [
            r"pela defesa de", r"pela ordem, excelência", r"doutor, nessa investigação",
            r"gostaria de saber", r"o senhor chegou a ver o meu cliente", r"havia alguma droga com ele",
            r"sem perguntas pela defesa", r"a defesa insiste na pergunta", r"excelência, pela defesa",
            r"como o senhor conseguiu", r"conseguiu identificar", r"o senhor sabe dizer se"
        ]
    }

    def __init__(
        self,
        mode: str = "audiencia",
        depoente: Optional[str] = None,
        speakers_list: Optional[List[str]] = None,
        speaker_schedule: Optional[Dict[Tuple[float, float], str]] = None
    ):
        self.mode = mode
        self.depoente = depoente or ("Del. Rodrigo Moreira" if "rodrigo" in (depoente or "").lower() else "Depoente / Testemunha")
        self.speakers_list = speakers_list or []
        self.speaker_schedule = speaker_schedule or {}

    def diarize(self, segments: List[Dict[str, Any]], time_offset: float = 0.0) -> List[Dict[str, Any]]:
        diarized = []
        current_speaker = "Juiz(a) Presidente" if self.mode == "audiencia" else "Interlocutor 1"
        last_end = 0.0

        for seg in segments:
            seg_start = seg["start"] + time_offset
            seg_end = seg["end"] + time_offset
            text = seg["text"].strip()
            text_lower = text.lower()

            assigned = None

            # 1. Agendamento explícito por intervalo
            if self.speaker_schedule:
                for (t0, t1), spk in self.speaker_schedule.items():
                    if t0 <= seg_start <= t1:
                        assigned = spk
                        break

            # 2. Modo Interceptação Telefônica
            if not assigned and self.mode == "interceptacao":
                if self.speakers_list and len(self.speakers_list) >= 2:
                    # Alternância simples ou por menções
                    assigned = self.speakers_list[0] if current_speaker != self.speakers_list[0] else self.speakers_list[1]
                else:
                    assigned = "Alvo / Investigado" if current_speaker != "Alvo / Investigado" else "Interlocutor"

            # 3. Modo Audiência Judicial (AIJ)
            if not assigned and self.mode == "audiencia":
                if any(re.search(p, text_lower) for p in self.ROLE_PATTERNS["Magistrado(a)"]):
                    assigned = "Juiz(a) Presidente"
                elif any(re.search(p, text_lower) for p in self.ROLE_PATTERNS["Promotor(a) de Justiça"]):
                    assigned = "Promotor(a) de Justiça"
                elif any(re.search(p, text_lower) for p in self.ROLE_PATTERNS["Advogado(a) de Defesa"]):
                    assigned = "Advogado(a) de Defesa"
                elif text_lower.startswith(("não, não", "não,", "não foi", "sim,", "sim.", "olha, doutor", "doutora,", "excelência,", "a investigação começou", "nós começamos")):
                    assigned = self.depoente
                elif text.endswith("?"):
                    # Se termina com interrogação, quem está falando é o inquiridor da vez
                    if current_speaker == self.depoente:
                        assigned = "Advogado(a) de Defesa" if "doutor" in text_lower or "senhor" in text_lower else "Juiz(a) / MP"
                    else:
                        assigned = current_speaker
                else:
                    # Se houve pausa após uma pergunta, a resposta é do depoente
                    pause = seg["start"] - last_end
                    if pause > 0.6 and current_speaker != self.depoente:
                        assigned = self.depoente
                    else:
                        assigned = current_speaker

            current_speaker = assigned
            last_end = seg["end"]

            item = dict(seg)
            item["start_adjusted"] = round(seg_start, 3)
            item["end_adjusted"] = round(seg_end, 3)
            item["speaker"] = current_speaker
            diarized.append(item)

        # 4. Fusão de falas consecutivas do mesmo orador com intervalo curto
        merged = self._merge_consecutive_speeches(diarized)
        return merged

    def _merge_consecutive_speeches(self, segments: List[Dict[str, Any]], max_gap: float = 1.8) -> List[Dict[str, Any]]:
        """Une falas contíguas do mesmo orador para gerar parágrafos coesos e citações fluidas."""
        if not segments:
            return []

        merged_list = []
        curr = dict(segments[0])

        for nxt in segments[1:]:
            gap = nxt["start_adjusted"] - curr["end_adjusted"]
            # Mesmo orador e intervalo pequeno
            if nxt["speaker"] == curr["speaker"] and gap <= max_gap:
                # Concatena o texto
                curr["end_adjusted"] = nxt["end_adjusted"]
                curr["end"] = nxt["end"]
                curr["text"] = f"{curr['text']} {nxt['text']}".strip()
                if "words" in curr and "words" in nxt:
                    curr["words"] = curr["words"] + nxt["words"]
            else:
                merged_list.append(curr)
                curr = dict(nxt)

        merged_list.append(curr)
        # Reatribui IDs ordenados
        for idx, m in enumerate(merged_list, start=1):
            m["id"] = idx
        return merged_list


# ==============================================================================
# AUDITORIA FORENSE DE TERMOS-CHAVE
# ==============================================================================
class CriminalKeywordsAuditor:
    """Varre a transcrição em busca de termos sensíveis da dogmática e processo penal."""

    def __init__(self, custom_keywords: Optional[Dict[str, List[str]]] = None):
        self.categories = dict(DEFAULT_CRIMINAL_KEYWORDS)
        if custom_keywords:
            for cat, terms in custom_keywords.items():
                if cat in self.categories:
                    self.categories[cat].extend(terms)
                else:
                    self.categories[cat] = terms

    def audit(self, diarized_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        findings_by_category: Dict[str, List[Dict[str, Any]]] = {}
        total_occurrences = 0

        for category, terms in self.categories.items():
            findings_by_category[category] = []
            compiled_terms = [re.escape(t.lower()) for t in terms]
            pattern = re.compile(r"\b(" + "|".join(compiled_terms) + r")\b", re.IGNORECASE)

            for seg in diarized_segments:
                text = seg["text"]
                matches = list(pattern.finditer(text))
                if matches:
                    matched_words = list(set(m.group(0).lower() for m in matches))
                    timestamp_str = format_timestamp(seg["start_adjusted"])
                    impact = self._evaluate_impact(text.lower(), matched_words)

                    findings_by_category[category].append({
                        "segment_id": seg["id"],
                        "timestamp": timestamp_str,
                        "start_seconds": seg["start_adjusted"],
                        "speaker": seg["speaker"],
                        "matched_terms": matched_words,
                        "text": text,
                        "impact": impact
                    })
                    total_occurrences += len(matches)

        return {
            "total_occurrences": total_occurrences,
            "categories": findings_by_category
        }

    def _evaluate_impact(self, text_lower: str, matched_terms: List[str]) -> Dict[str, str]:
        # Tese 1: Afastamento de facção criminosa ou organização
        if "facção" in text_lower and any(neg in text_lower for neg in ["não", "nenhum", "afasta", "descart"]):
            return {
                "tipo": "ALTAMENTE FAVORÁVEL À DEFESA (Afastamento do Art. 35 / Facção)",
                "detalhe": "Declaração expressa afastando existência de facção criminosa ou estrutura estável/armada."
            }
        # Tese 2: Ausência de materialidade direta / sem apreensão com o réu
        if "droga" in text_lower and any(neg in text_lower for neg in ["não foi encontrada", "não apreendeu", "nenhuma", "sem apreensão", "não tinha nada"]):
            return {
                "tipo": "ALTAMENTE FAVORÁVEL À DEFESA (Falta de Materialidade Direta)",
                "detalhe": "Indicação de que nenhuma substância entorpecente foi apreendida diretamente em posse do cliente."
            }
        # Tese 3: Ausência de hierarquia ou subordinação
        if "hierarquia" in text_lower and any(neg in text_lower for neg in ["não havia", "sem hierarquia", "desorganizado", "não tinha chefe"]):
            return {
                "tipo": "ALTAMENTE FAVORÁVEL À DEFESA (Descaracterização de Hierarquia)",
                "detalhe": "Afastamento do elemento subjetivo e estrutural do Art. 35 da Lei 11.343/06."
            }
        # Ponto acusatório
        if any(c in text_lower for c in ["confessou", "flagrante", "apreendido com ele"]):
            return {
                "tipo": "PONTO DE ATENÇÃO ACUSATÓRIO",
                "detalhe": "Elemento de convicção utilizado pela acusação que demanda contraposição técnica ou nulidade."
            }
        return {
            "tipo": "RELEVANTE / CONTEXTUAL",
            "detalhe": f"Menção aos termos processuais: {', '.join(matched_terms)}."
        }


# ==============================================================================
# GERADOR DE CITAÇÕES JURÍDICAS FORMATADAS
# ==============================================================================
class LegalCitationGenerator:
    """Gera blocos de citação formatados conforme os padrões das Cortes Superiores e do SuperJus."""

    def __init__(self, processo: Optional[str] = None, vara: Optional[str] = None, orgao: Optional[str] = None, mode: str = "audiencia"):
        self.processo = processo or "Ação Penal Originária"
        self.vara = vara or "Juízo Criminal de Origem"
        self.orgao = orgao or "Poder Judiciário"
        self.mode = mode

    def _get_source_label(self, timestamp_str: str) -> str:
        if self.mode == "interceptacao":
            return f"*(Fonte: Interceptação Telefônica / Mídia de Áudio — Autos do Processo {self.processo}, {self.vara}, carimbo temporal [{timestamp_str}])*"
        elif self.mode == "tribunal_juri":
            return f"*(Fonte: Sessão Plenária do Tribunal do Júri — Ação Penal {self.processo}, {self.vara}, evento aos [{timestamp_str}])*"
        elif self.mode == "reuniao_teams":
            return f"*(Fonte: Gravação de Audiência Virtual / Teams — Autos do Processo {self.processo}, {self.vara}, aos [{timestamp_str}])*"
        return f"*(Fonte: Mídia da Audiência de Instrução e Julgamento — Ação Penal {self.processo}, {self.vara}, evento aos [{timestamp_str}])*"

    def generate_citations(
        self,
        diarized_segments: List[Dict[str, Any]],
        audit_results: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        citations = []

        for seg in diarized_segments:
            text = seg["text"].strip()
            speaker = seg["speaker"]
            timestamp_str = format_timestamp(seg["start_adjusted"])
            source_label = self._get_source_label(timestamp_str)

            # Formato padrão SuperJus para inserção direta em peças
            formatted_quote = (
                f"> *\"[{timestamp_str}] {speaker}: \\\"{text}\\\"\"*\n"
                f"> {source_label}"
            )

            compact_quote = f"[{timestamp_str}] {speaker}: \"{text}\""

            citations.append({
                "segment_id": seg["id"],
                "timestamp": timestamp_str,
                "speaker": speaker,
                "text": text,
                "formatted_quote": formatted_quote,
                "compact_quote": compact_quote
            })

        return citations


# ==============================================================================
# EXPORTADORES FORENSES MULTI-FORMATO
# ==============================================================================
class ForensicExporters:
    """Exporta relatórios em TXT, MD, SRT, JSON, Dossiê de Auditoria e Citações Jurídicas."""

    @staticmethod
    def export_all(
        base_dir: str,
        base_name: str,
        diarized_segments: List[Dict[str, Any]],
        audit_data: Dict[str, Any],
        citations_data: List[Dict[str, Any]],
        metadata: Dict[str, Any],
        processo: str,
        vara: str
    ) -> Dict[str, str]:
        os.makedirs(base_dir, exist_ok=True)
        paths = {}

        # 1. Transcrição Contínua TXT
        txt_path = os.path.join(base_dir, f"{base_name}_transcricao_completa.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"=== TRANSCRIÇÃO INTEGRAL DE MÍDIA FORENSE ===\n")
            f.write(f"Processo: {processo} | Vara: {vara}\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
            for s in diarized_segments:
                t_start = format_timestamp(s["start_adjusted"], include_millis=True)
                t_end = format_timestamp(s["end_adjusted"], include_millis=True)
                f.write(f"[{t_start} -> {t_end}]  {s['speaker']}: {s['text']}\n")
        paths["txt"] = txt_path

        # 2. Legendas SRT
        srt_path = os.path.join(base_dir, f"{base_name}_legendas.srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            for idx, s in enumerate(diarized_segments, start=1):
                t_start = format_timestamp(s["start_adjusted"], include_millis=True)
                t_end = format_timestamp(s["end_adjusted"], include_millis=True)
                f.write(f"{idx}\n{t_start} --> {t_end}\n{s['speaker']}: {s['text']}\n\n")
        paths["srt"] = srt_path

        # 3. Transcrição Estruturada Markdown
        md_path = os.path.join(base_dir, f"{base_name}_transcricao_formatada.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# ⚖️ Transcrição Forense de Audiência / Mídia Processual\n\n")
            f.write(f"- **Processo:** `{processo}`\n")
            f.write(f"- **Juízo:** {vara}\n")
            f.write(f"- **Data da Extração:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"- **Motor Whisper:** {metadata.get('engine', 'faster-whisper')} (modelo `{metadata.get('model', 'base')}`)\n\n")
            f.write(f"---\n\n## 🎙️ Diálogo Cronológico com Oradores e Timestamps\n\n")

            for s in diarized_segments:
                t_str = format_timestamp(s["start_adjusted"])
                f.write(f"**`[{t_str}]` {s['speaker']}:**\n")
                f.write(f"> {s['text']}\n\n")
        paths["md"] = md_path

        # 4. Dossiê de Auditoria de Termos-Chave
        audit_path = os.path.join(base_dir, f"{base_name}_auditoria_termos_chave.md")
        with open(audit_path, "w", encoding="utf-8") as f:
            f.write(f"# 🔍 Dossiê de Auditoria Penal de Termos-Chave\n\n")
            f.write(f"- **Processo de Referência:** `{processo}`\n")
            f.write(f"- **Total de Ocorrências Sensíveis Mapeadas:** {audit_data['total_occurrences']}\n\n")
            f.write(f"---\n\n")

            for cat_name, items in audit_data["categories"].items():
                f.write(f"## 📌 Categoria: {cat_name} ({len(items)} ocorrências)\n\n")
                if not items:
                    f.write(f"*Nenhuma ocorrência registrada nesta categoria.*\n\n")
                    continue

                for item in items:
                    f.write(f"### ⏱️ `[{item['timestamp']}]` — {item['speaker']}\n")
                    f.write(f"- **Termos Localizados:** `{', '.join(item['matched_terms'])}`\n")
                    f.write(f"- **Impacto Estratégico:** **{item['impact']['tipo']}** ({item['impact']['detalhe']})\n")
                    f.write(f"- **Declaração Transcrita:**\n")
                    f.write(f"  > *\"{item['text']}\"*\n\n")
        paths["auditoria"] = audit_path

        # 5. Citações Jurídicas Prontas para Peças
        citations_path = os.path.join(base_dir, f"{base_name}_citacoes_juridicas.md")
        with open(citations_path, "w", encoding="utf-8") as f:
            f.write(f"# 📜 Citações Jurídicas Formatadas para Peças Processuais\n\n")
            f.write(f"*(Prontas para copiar e colar em Habeas Corpus, Memoriais, Resposta à Acusação e Apelação)*\n\n")
            f.write(f"- **Processo Vinculado:** `{processo}`\n")
            f.write(f"- **Vara / Comarca:** {vara}\n\n")
            f.write(f"---\n\n## 🎯 Trechos Probatórios Selecionados\n\n")

            highlighted_count = 0
            for cit in citations_data:
                seg_id = cit["segment_id"]
                matched_impact = None
                for cat_items in audit_data["categories"].values():
                    for item in cat_items:
                        if item["segment_id"] == seg_id:
                            matched_impact = item["impact"]
                            break
                    if matched_impact:
                        break

                if matched_impact:
                    highlighted_count += 1
                    f.write(f"### Citação #{highlighted_count} — [{cit['timestamp']}] {cit['speaker']}\n")
                    f.write(f"**Relevância Estratégica:** {matched_impact['tipo']}\n")
                    f.write(f"**Fundamento:** *{matched_impact['detalhe']}*\n\n")
                    f.write(f"#### Bloquete para Petição Judicial (Markdown):\n\n")
                    f.write(f"{cit['formatted_quote']}\n\n")
                    f.write(f"```markdown\n{cit['formatted_quote']}\n```\n\n---\n\n")

            if highlighted_count == 0:
                for cit in citations_data[:10]:
                    f.write(f"{cit['formatted_quote']}\n\n---\n\n")
        paths["citacoes"] = citations_path

        # 6. JSON Estruturado
        json_path = os.path.join(base_dir, f"{base_name}_transcricao.json")
        full_payload = {
            "metadata": metadata,
            "processo": processo,
            "vara": vara,
            "audit_summary": {
                "total_occurrences": audit_data["total_occurrences"],
            },
            "segments": diarized_segments
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(full_payload, f, ensure_ascii=False, indent=2)
        paths["json"] = json_path

        return paths


# ==============================================================================
# INTEGRAÇÃO COM MEMU (MEMÓRIA PERSISTENTE)
# ==============================================================================
def persist_in_memu(
    processo: str,
    base_name: str,
    audit_data: Dict[str, Any],
    citations_data: List[Dict[str, Any]]
) -> bool:
    """Grava os achados probatórios da transcrição na base memU do SuperJus."""
    script_memu = os.path.join(os.path.dirname(__file__), "memu_store.py")
    if not os.path.exists(script_memu):
        print("[!] Script scripts/memu_store.py não encontrado.")
        return False

    favoraveis = []
    for cat, items in audit_data["categories"].items():
        for it in items:
            if "FAVORÁVEL" in it["impact"]["tipo"]:
                favoraveis.append(f"- [{it['timestamp']}] {it['speaker']}: \"{it['text']}\" ({it['impact']['detalhe']})")

    content_lines = [
        f"# Transcrição e Auditoria Forense — {base_name}",
        f"**Processo:** `{processo}`",
        f"**Data da Auditoria:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"**Total de Ocorrências Sensíveis:** {audit_data['total_occurrences']}",
        "",
        "## 🛡️ Principais Declarações Favoráveis à Defesa Localizadas:",
    ]
    if favoraveis:
        content_lines.extend(favoraveis[:10])
    else:
        content_lines.append("*Nenhum elemento expressamente favorável ou desfavorável isolado.*")

    content = "\n".join(content_lines)
    mem_name = f"auditoria_audiencia_{base_name[:30].replace(' ', '_')}.md"
    desc = f"Auditoria de mídia/audiência com Whisper para o processo {processo} ({len(favoraveis)} teses identificadas)"

    cmd = [
        sys.executable,
        script_memu,
        "--name", mem_name,
        "--track", "Julio_Pereira_Marcos_Caso_Principal" if "0023013" in processo or "0022975" in processo else "memory",
        "--description", desc,
        "--content", content
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", check=False)
        if res.returncode == 0:
            print("[+] Memória persistida no memU com sucesso!")
            return True
        else:
            print(f"[!] Aviso: retorno do memU: {res.stderr.strip() or res.stdout.strip()}")
            return False
    except Exception as e:
        print(f"[!] Erro ao chamar memu_store.py: {e}")
        return False


# ==============================================================================
# PIPELINE PRINCIPAL DE PROCESSAMENTO
# ==============================================================================
def process_single_media(
    media_path: str,
    args: argparse.Namespace,
    whisper_engine: WhisperEngine,
    auditor: CriminalKeywordsAuditor
) -> Dict[str, str]:
    """Processa um único arquivo de mídia do início ao fim."""
    print(f"\n{'='*70}")
    print(f"[*] INICIANDO AUDITORIA FORENSE: {os.path.basename(media_path)}")
    print(f"{'='*70}")

    audio_path, is_temp = MediaManager.extract_audio_if_needed(media_path)

    try:
        raw_segments, metadata = whisper_engine.transcribe(
            audio_path,
            language=args.language,
            beam_size=args.beam_size,
            word_timestamps=True
        )

        if not raw_segments:
            print("[!] Nenhum segmento de fala detectado na mídia.")
            return {}

        # 1. Refinamento de turnos dialógicos com base em palavras e interrogações
        split_segments = TurnRefiner.split_on_dialog_turns(raw_segments)

        # 2. Diarização e Atribuição de Oradores
        speakers_list = [s.strip() for s in args.speakers.split(",")] if args.speakers else []
        diarizer = SpeakerDiarizer(
            mode=args.mode,
            depoente=args.depoente,
            speakers_list=speakers_list
        )
        diarized_segments = diarizer.diarize(split_segments, time_offset=args.offset_seconds)

        # 3. Auditoria de Termos-Chave
        audit_data = auditor.audit(diarized_segments)
        print(f"[+] Auditoria concluída: {audit_data['total_occurrences']} termos sensíveis identificados.")

        # 4. Geração de Citações Jurídicas
        cit_gen = LegalCitationGenerator(
            processo=args.processo,
            vara=args.vara,
            mode=args.mode
        )
        citations_data = cit_gen.generate_citations(diarized_segments, audit_data)

        # 5. Exportação dos Relatórios Forenses
        output_dir = args.output_dir or os.path.dirname(media_path) or "."
        base_name = os.path.splitext(os.path.basename(media_path))[0]
        exported_paths = ForensicExporters.export_all(
            base_dir=output_dir,
            base_name=base_name,
            diarized_segments=diarized_segments,
            audit_data=audit_data,
            citations_data=citations_data,
            metadata=metadata,
            processo=args.processo,
            vara=args.vara
        )

        print(f"\n[+] ARQUIVOS FORENSES GERADOS COM SUCESSO:")
        for k, p in exported_paths.items():
            print(f"    - {k.upper():10s}: {p}")

        if args.memu or ("0023013" in args.processo):
            print(f"[*] Registrando achados no memU...")
            persist_in_memu(args.processo, base_name, audit_data, citations_data)

        return exported_paths

    finally:
        if is_temp and os.path.exists(audio_path):
            try:
                os.unlink(audio_path)
            except Exception:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="Módulo de Transcrição e Auditoria de Audiências e Interceptações Telefônicas com Whisper — SuperJus",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", "-i", help="Caminho do arquivo de áudio ou vídeo a transcrever")
    group.add_argument("--dir", "-d", help="Pasta com múltiplos arquivos de áudio/vídeo para processar em lote")

    parser.add_argument("--output-dir", "-o", help="Diretório para salvar os relatórios (default: mesma pasta da mídia)")
    parser.add_argument("--model", "-m", default="base", choices=["tiny", "base", "small", "medium", "large-v2", "large-v3", "turbo"], help="Modelo do Whisper (default: base)")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"], help="Dispositivo de execução (default: auto)")
    parser.add_argument("--language", "-l", default="pt", help="Código do idioma (default: pt)")
    parser.add_argument("--beam-size", type=int, default=5, help="Beam size para transcrição (default: 5)")
    parser.add_argument("--offset-seconds", type=float, default=0.0, help="Offset temporal em segundos para mídias fatiadas (ex: 1235.0)")
    parser.add_argument("--mode", default="audiencia", choices=["audiencia", "interceptacao", "tribunal_juri", "reuniao_teams"], help="Modo de análise (default: audiencia)")
    parser.add_argument("--depoente", help="Nome/Cargo do depoente principal (ex: 'Del. Rodrigo Moreira')")
    parser.add_argument("--speakers", help="Lista de oradores separados por vírgula (ex: 'Juiz,Promotor,Del. Rodrigo Moreira,Defensor')")
    parser.add_argument("--processo", default="0023013-51.2021.8.19.0078", help="Número da Ação Penal de referência")
    parser.add_argument("--vara", default="1ª Vara de Armação dos Búzios/RJ", help="Vara / Comarca de origem")
    parser.add_argument("--keywords", help="Termos-chave adicionais separados por vírgula para auditoria")
    parser.add_argument("--memu", action="store_true", help="Grava sumário dos achados na memória memU")

    args = parser.parse_args()

    engine = WhisperEngine(model_name=args.model, device=args.device)

    custom_dict = {}
    if args.keywords:
        extra_terms = [k.strip() for k in args.keywords.split(",") if k.strip()]
        custom_dict["Termos Personalizados do Usuário"] = extra_terms
    auditor = CriminalKeywordsAuditor(custom_dict if custom_dict else None)

    media_files = []
    if args.input:
        if not os.path.exists(args.input):
            print(f"[!] Erro: Arquivo {args.input} não encontrado.")
            sys.exit(1)
        media_files.append(args.input)
    elif args.dir:
        if not os.path.exists(args.dir):
            print(f"[!] Erro: Diretório {args.dir} não encontrado.")
            sys.exit(1)
        for root, _, files in os.walk(args.dir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in MediaManager.AUDIO_EXTENSIONS or ext in MediaManager.VIDEO_EXTENSIONS:
                    media_files.append(os.path.join(root, f))

    if not media_files:
        print("[!] Nenhuma mídia multimídia válida encontrada.")
        sys.exit(0)

    print(f"\n[+] Total de mídias identificadas para processamento: {len(media_files)}")
    for mf in media_files:
        process_single_media(mf, args, engine, auditor)

    print("\n[✔] Processamento e Auditoria Forense concluídos com sucesso!")


if __name__ == "__main__":
    main()
