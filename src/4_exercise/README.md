# 🤖 Question Generator AI Agent

Inteligentní AI agent pro automatické generování otázek v českém jazyce. Agent využívá Wikipedia jako zdroj informací a ukládá vygenerované otázky do SQLite databáze.

## ✨ Hlavní funkce

- **🔍 Vyhledávání témat** - Prohledává existující témata v databázi
- **📝 Generování otázek** - Automaticky vytváří otázky na základě Wikipedia článků
- **💾 Správa databáze** - Ukládá témata a otázky v SQLite databázi
- **🌐 Wikipedia integrace** - Získává informace z českých a anglických článků
- **💬 Konverzační rozhraní** - Přirozená komunikace s uživatelem

## 🛠️ Technologie

- **LangGraph** - Framework pro AI workflow
- **OpenAI GPT-4** - Jazykový model pro generování otázek
- **SQLite** - Databáze pro ukládání témat a otázek
- **Wikipedia API** - Zdroj informací pro generování otázek
- **Python**

## 📋 Požadavky

```bash
pip install langgraph langchain-openai wikipedia sqlite3
```

Nastavte OpenAI API klíč:
```bash
export OPENAI_API_KEY="your-api-key"
```

## 💡 Ukázka použití

```
🤖 Vítejte v AI Agentovi pro generování otázek!
Jsem váš inteligentní asistent pro vytváření a správu otázek.

❓ Vaše volba: Zajímá mě téma o kočkách
🤖 Agent rozhoduje...
💬 Agent odpověděl: 
 Téma "kočka" již existuje v databázi pod ID 1. Pokud vás zajímají otázky k tomuto tématu nebo chcete jinou akci, dejte mi vědět.

❓ Vaše volba: Téma vesmír
🤖 Agent rozhoduje...
💬 Agent odpověděl: 
 Téma "vesmír" zatím v databázi neexistuje. Chcete toto téma vytvořit a vygenerovat k němu otázky?

❓ Vaše volba: ano
🤖 Agent rozhoduje...
💬 Agent odpověděl: 
 Na základě informací z Wikipedie o vesmíru jsem vygeneroval následující otázky:
1. Co rozumíme pod pojmem vesmír?
2. Jaký je původ slova "kosmos" a co znamená?
3. Co všechno zahrnuje pojem vesmír?
Chcete tyto otázky uložit do databáze pod novým tématem "vesmír"?

❓ Vaše volba: ano
🤖 Agent rozhoduje...
💬 Agent odpověděl: 
 Téma "vesmír" bylo úspěšně vytvořeno s ID 2 a k němu byly přidány 3 otázky do databáze.

❓ Vaše volba: Jaké máme otázky k tématu kočky?
🤖 Agent rozhoduje...
💬 Agent odpověděl: 
 K tématu "kočka" máme v databázi následující otázky:
1. Jaké je latinské označení pro kočku domácí?
2. Do jaké podčeledi patří kočka domácí?
3. Proč byla kočka domestikována člověkem?
4. Jak je zrak, sluch a čich u kočky domácí?
5. Kde se konzumuje kočičí maso?
6. Byl dovoz kočičí kůže do Evropské unie zakázán?
7. Kde se kočka domácí nevyskytuje?
8. Je kočka domácí efektivním lovce?
9. Jaké druhy zvířat kočka domácí loví?

❓ Vaše volba: to je vše, ukončit
🤖 Agent rozhoduje...
Process finished with exit code 0
```

## 🗃️ Databázová struktura

### Tabulka `topics`
- `id` - Unikátní identifikátor tématu
- `name` - Název tématu
- `description` - Popis tématu (max 255 znaků)

### Tabulka `questions`
- `id` - Unikátní identifikátor otázky
- `topic_id` - Odkaz na téma
- `question_text` - Text otázky



## ⚙️ Konfigurace

V souboru můžete nastavit:
- `DEBUG = True/False` - Zapnutí/vypnutí debug výstupů
- `DB_PATH` - Cesta k SQLite databázi
- `force_create_db` - Přepsání existující databáze

## 🔧 Architektura

Agent využívá LangGraph framework s následujícími komponenty:

- **Tools** - Funkce pro práci s databází a Wikipedia
- **State Management** - Správa konverzačního stavu
- **Workflow** - Řízení toku mezi nástroji a AI modelem
- **Memory** - Uchovávání kontextu konverzace
