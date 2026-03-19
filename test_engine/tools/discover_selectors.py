#!/usr/bin/env python3
"""
Selector Discovery Tool
=======================
Inspeciona a página de login de uma aplicação web e sugere os selectores
a colocar no appsettings.json do test_engine.

Uso:
    python3 test_engine/tools/discover_selectors.py
    python3 test_engine/tools/discover_selectors.py --url https://myapp.com --login-path #/login

Requisitos:
    pip install -r test_engine/tools/requirements.txt
    playwright install chromium
"""

import argparse
import json
import os
import sys
from pathlib import Path


def load_appsettings() -> dict:
    """Carrega appsettings.json relativo ao test_engine/."""
    script_dir = Path(__file__).parent
    appsettings_path = script_dir.parent / "appsettings.json"

    if not appsettings_path.exists():
        return {}

    with open(appsettings_path, encoding="utf-8") as f:
        return json.load(f)


def discover(base_url: str, login_path: str, headless: bool = True) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Erro: playwright não está instalado.")
        print("Corre: pip install playwright && playwright install chromium")
        sys.exit(1)

    browsers_path = os.environ.get(
        "PLAYWRIGHT_BROWSERS_PATH",
        str(Path(__file__).parent.parent.parent / ".cache" / "ms-playwright"),
    )
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_path

    login_url = base_url.rstrip("/") + "/" + login_path.lstrip("/")
    print(f"\nA inspecionar: {login_url}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto(login_url, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        inputs = page.query_selector_all("input")
        buttons = page.query_selector_all("button, [role='button'], [type='submit']")

        print("=" * 60)
        print("INPUTS ENCONTRADOS")
        print("=" * 60)

        suggestions = {"username": None, "password": None, "button": None}
        input_info = []

        for i, el in enumerate(inputs):
            info = {
                "type": el.get_attribute("type") or "-",
                "name": el.get_attribute("name") or "-",
                "id": el.get_attribute("id") or "-",
                "placeholder": el.get_attribute("placeholder") or "-",
                "data-cy": el.get_attribute("data-cy") or "-",
                "data-testid": el.get_attribute("data-testid") or "-",
                "class": (el.get_attribute("class") or "")[:40],
            }
            input_info.append(info)

            selector = _build_best_selector_for_input(info)

            typ = info["type"].lower()
            if typ in ("text", "email") and suggestions["username"] is None:
                suggestions["username"] = selector
            elif typ == "password" and suggestions["password"] is None:
                suggestions["password"] = selector

            print(f"  [{i+1}] type={info['type']} | name={info['name']} | id={info['id']}")
            print(f"       placeholder={info['placeholder']} | data-cy={info['data-cy']}")
            print(f"       Selector sugerido: {selector}")
            print()

        print("=" * 60)
        print("BOTÕES ENCONTRADOS")
        print("=" * 60)

        for i, el in enumerate(buttons):
            text = (el.inner_text() or "").strip()
            typ = el.get_attribute("type") or "-"
            data_cy = el.get_attribute("data-cy") or "-"
            data_testid = el.get_attribute("data-testid") or "-"

            if text and suggestions["button"] is None:
                if data_cy != "-":
                    btn_selector = f"[data-cy='{data_cy}']"
                elif data_testid != "-":
                    btn_selector = f"[data-testid='{data_testid}']"
                else:
                    btn_selector = f"text={text}"
                suggestions["button"] = btn_selector

            print(f"  [{i+1}] type={typ} | text='{text}' | data-cy={data_cy}")
            if text:
                print(f"       Selector sugerido: text={text}")
            print()

        browser.close()

    print("=" * 60)
    print("SUGESTÃO PARA appsettings.json")
    print("=" * 60)
    print()
    print(json.dumps({
        "UsernameSelector": suggestions["username"] or "input[type='text']",
        "PasswordSelector": suggestions["password"] or "input[type='password']",
        "LoginButtonSelector": suggestions["button"] or "button[type='submit']",
    }, indent=2, ensure_ascii=False))
    print()
    print("Copia estes campos para o appsettings.json do test_engine.")


def _build_best_selector_for_input(info: dict) -> str:
    """Constrói o melhor selector possível por ordem de preferência."""
    if info["data-cy"] != "-":
        return f"[data-cy='{info['data-cy']}']"
    if info["data-testid"] != "-":
        return f"[data-testid='{info['data-testid']}']"
    if info["id"] not in ("-",) and not info["id"].startswith(":"):
        return f"#{info['id']}"
    if info["name"] != "-":
        return f"input[name='{info['name']}']"
    if info["type"] != "-":
        return f"input[type='{info['type']}']"
    return "input"


def main() -> None:
    config = load_appsettings()

    parser = argparse.ArgumentParser(description="Descobre selectores da página de login.")
    parser.add_argument(
        "--url",
        default=config.get("BaseUrl", ""),
        help="URL base da aplicação (default: BaseUrl do appsettings.json)",
    )
    parser.add_argument(
        "--login-path",
        default=config.get("LoginPath", ""),
        help="Caminho de login (default: LoginPath do appsettings.json)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Abre o browser visível (útil para debug)",
    )

    args = parser.parse_args()

    if not args.url:
        print("Erro: fornece --url ou define BaseUrl no appsettings.json")
        sys.exit(1)

    discover(
        base_url=args.url,
        login_path=args.login_path,
        headless=not args.no_headless,
    )


if __name__ == "__main__":
    main()
