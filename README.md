# CPU Benchmark Script

This script is a simple CPU benchmark tool written in Python. It allows you to measure your CPU's performance by running a stress test for a defined duration and logging the results. It also provides an option to generate a graphical representation of past test results.

## Features
- Runs a CPU stress test for a configurable duration
- Logs CPU information, test duration, and temperatures (Linux only)
- Saves results in JSON format for future reference
- Generates a graph from stored results
- Supports English and Czech languages

## Installation

### Prerequisites
Make sure you have Python installed on your system. You also need `pip` to install dependencies.

### Clone the Repository
Run the following command to clone the repository:

```sh
git clone https://github.com/stepanvalic/CPU-benchmark.git
cd CPU-benchmark
```

### Install Required Packages
Run the following command to install the necessary dependencies:

```sh
pip install -r requirements.txt
```

For Linux users, install `lm-sensors` to enable CPU temperature monitoring:

```sh
sudo apt-get install lm-sensors
sudo sensors-detect
```

## Usage

Run the script using:

```sh
python benchmark.py
```

### Options
When prompted, you can:
1. Run a new CPU test
2. Generate a graph from stored results

### Output
- Test results are saved in the `completed_tests` directory in JSON format.
- If you choose to generate a graph, you can either display it or export it as an image.

## Notes
- CPU temperature monitoring is only available on Linux.
- On Windows, temperature data is not currently supported.

---

# CS - Czech

# CPU Benchmark Skript

Tento skript je jednoduchý nástroj pro měření výkonu CPU. Umožňuje spustit zátěžový test procesoru, zaznamenat výsledky a vygenerovat graf z uložených dat.

## Funkce
- Spustí zátěžový test CPU na definovanou dobu
- Uloží informace o CPU, délku testu a teploty (pouze Linux)
- Výsledky ukládá ve formátu JSON
- Generuje graf z předchozích výsledků
- Podporuje anglický a český jazyk

## Instalace

### Požadavky
Ujistěte se, že máte nainstalovaný Python a `pip` pro instalaci balíčků.

### Klonování repozitáře
Spusťte následující příkaz pro klonování repozitáře:

```sh
git clone https://github.com/stepanvalic/CPU-benchmark.git
cd CPU-benchmark
```

### Instalace potřebných balíčků
Spusťte příkaz:

```sh
pip install -r requirements.txt
```

Pro uživatele Linuxu je potřeba nainstalovat `lm-sensors`, aby bylo možné sledovat teploty CPU:

```sh
sudo apt-get install lm-sensors
sudo sensors-detect
```

## Použití

Skript spustíte příkazem:

```sh
python benchmark.py
```

### Možnosti
Po spuštění si můžete vybrat:
1. Spustit nový CPU test
2. Vygenerovat graf z uložených výsledků

### Výstup
- Výsledky testu se ukládají do složky `completed_tests` ve formátu JSON.
- Pokud se rozhodnete vytvořit graf, můžete si ho zobrazit nebo exportovat jako obrázek.

## Poznámky
- Sledování teplot CPU je dostupné pouze na Linuxu.
- Na Windows není podpora pro zobrazování teplot implementována.
