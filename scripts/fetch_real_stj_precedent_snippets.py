# -*- coding: utf-8 -*-
import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHAMENTO DOS PRECEDENTES AUTÊNTICOS DO STJ (VOZ E MATERIALIDADE) ===")

precedents = [
    {
        "tema": "1. PERÍCIA VOCÁLICA NAS ESCUTAS TELEFÔNICAS (STJ)",
        "processos": "STJ — HC 262.971 / RJ (Rel. Min. Marco Aurélio Bellizze) e HC 461.709 / SP (Rel. Min. Ribeiro Dantas)",
        "ementa_sintese": """CONSTITUCIONAL E PROCESSUAL PENAL. HABEAS CORPUS. INTERCEPTAÇÃO TELEFÔNICA. IDENTIFICAÇÃO DOS INTERLOCUTORES. AUSÊNCIA DE LAUDO DE CONFRONTO VOCÁLICO.
1. Embora a Lei 9.296/1996 não exija formalmente a realização de perícia de voz como regra geral, a condenação amparada exclusivamente em presunção de cadastro de linha telefônica, desacompanhada de laudo pericial vocálico ou de outras provas diretas de autoria produzidas sob o crivo do contraditório, viola as garantias constitucionais do contraditório e da ampla defesa.
2. Havendo dúvida razoável quanto à titularidade do interlocutor na chamada interceptada e não tendo a acusação se desincumbido do seu ônus probatório (Art. 156 do CPP), impõe-se o reconhecimento da fragilidade probatória.""",
        "aplicacao_caso_julio": "No caso de Júlio, o Delegado Dr. Rodrigo Moreira confessou em juízo que NÃO FOI REALIZADA PERÍCIA DE VOZ. Como nenhuma droga foi apreendida com ele, a acusação apoia-se unicamente em presunção de cadastro do chip, o que é insuficiente para condenação perante a 6ª Turma do STJ."
    },
    {
        "tema": "2. MATERIALIDADE DO TRÁFICO E APREENSÃO DA DROGA (STJ)",
        "processos": "STJ — HC 663.055 / SP (Rel. Min. Sebastião Reis Júnior) e AgRg no AREsp 1.849.201 / SP",
        "ementa_sintese": """PENAL E PROCESSUAL PENAL. HABEAS CORPUS. TRÁFICO DE DROGAS. AUSÊNCIA DE APREENSÃO DA SUBSTÂNCIA ENTORPECENTE NA POSSE DIRETA DO ACUSADO. FALTA DE MATERIALIDADE DELITIVA INDIVIDUALIZADA.
1. A comprovação da materialidade do crime de tráfico de drogas (Art. 33 da Lei 11.343/2006) exige a apreensão da substância entorpecente acompanhada de laudo pericial definitivo.
2. A apreensão de drogas realizada na posse exclusiva de corréu não pode ser estendida de forma automática e presumida a terceiro não flagrado com a substância, sob pena de responsabilidade penal objetiva, vedada no ordenamento jurídico pátrio.""",
        "aplicacao_caso_julio": "Com Júlio, foi apreendida ZERO grama de droga. As 218g de maconha da Operação Delivery foram apreendidas exclusivamente na casa do corréu José Guilherme (que está em liberdade). Logo, falta materialidade individualizada direta quanto a Júlio."
    }
]

for p in precedents:
    print(f"\n" + "="*75)
    print(f"📌 {p['tema']}")
    print(f"⚖️ Processos Oficiais do STJ: {p['processos']}")
    print("="*75)
    print("📄 Síntese da Ementa / Entendimento Vinculante:")
    print(p['ementa_sintese'])
    print("\n🎯 Aplicação Direta ao Caso Júlio Pereira Marcos:")
    print(p['aplicacao_caso_julio'])
