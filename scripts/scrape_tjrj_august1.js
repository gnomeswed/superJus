const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
    console.log("Iniciando busca TJRJ para 01/08/2026...");
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
        await page.goto("https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica", { waitUntil: "domcontentloaded", timeout: 60000 });
        await page.waitForTimeout(4000);

        const frame = page.frameLocator("iframe#mainframe");
        await frame.locator("input[name='numeroProcesso']").fill("0023013-51.2021.8.19.0078");
        await page.waitForTimeout(1000);
        await frame.locator("#botaoPesquisarProcesso, button:has-text('Pesquisar')").first().click();
        await page.waitForTimeout(6000);

        try {
            await frame.locator("button:has-text('Todos Os Movimentos')").first().click();
            await page.waitForTimeout(4000);
        } catch (e) {
            console.log("Aviso no botão todos os movimentos:", e.message);
        }

        const realFrame = await page.querySelector("iframe#mainframe").contentFrame();
        const text = await realFrame.innerText("body");

        fs.writeFileSync("c:/Projetos/superJus/tjrj_live_august1_node.txt", text, "utf8");
        console.log("SUCESSO: Salvo em tjrj_live_august1_node.txt");
    } catch (e) {
        console.error("Erro no Playwright Node:", e);
    } finally {
        await browser.close();
    }
})();
