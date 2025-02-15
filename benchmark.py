import multiprocessing
import time
import platform
import psutil
import cpuinfo
import json
import os
import datetime
import matplotlib.pyplot as plt
import subprocess
import requests

LANG = "cs"

# Localization
locales = {
    "en": {
        "starting_benchmark": "Starting CPU benchmark...",
        "benchmark_completed": "Benchmark completed.",
        "cpu_info": "CPU Information:",
        "cpu_temperatures": "CPU Temperatures:",
        "temp_not_available": "Temperature data not available",
        "test_duration": "Test Duration: {time:.2f} seconds",
        "run_test": "Press 1 to run the CPU test",
        "generate_graph": "Press 2 to generate a graph from stored data",
        "invalid_input": "Invalid input, exiting.",
        "installing_pyspectator": "Installing pyspectator for Windows...",
        "installing_lm_sensors": "Installing lm-sensors for Linux...",
        "results_saved": "Results saved to {filename}",
        "no_test_data": "No test data available.",
        "unsupported_os": "Unsupported operating system.",
        "graph_title": "CPU Benchmark Results",
        "graph_xlabel": "Timestamp",
        "graph_ylabel": "Test Duration (s)",
        "enter_duration": "Enter the duration of the test in seconds (default is 20): ",
        "installing_pyspectator_excuse": "I'm sorry, but my experience with reading temperatures for windows is not good, so it won't be here yet.",
        "display_or_export": "Do you want to display the graph in a window (1) or export it to an image file (2)? ",
        "export_format": "Enter the desired export format (png, svg, jpeg, etc.): ",
        "export_success": "Graph successfully exported to {filename}",
        "export_failed": "Failed to export the graph.",
        "invalid_export_format": "Invalid export format.",
        "display_failed": "Failed to display the graph. Exporting to SVG instead.",
        "latest_version": "Latest version available: {version}",
        "check_updates": "Check for updates at: {url}",
        "update_failed": "Failed to check for updates.",
        "connection_error": "Could not connect to GitHub to check for updates.",
    },
    "cs": {
        "starting_benchmark": "Spuštění CPU benchmarku...",
        "benchmark_completed": "Benchmark dokončen.",
        "cpu_info": "Informace o CPU:",
        "cpu_temperatures": "Teploty CPU:",
        "temp_not_available": "Teplotní údaje nejsou k dispozici",
        "test_duration": "Doba testu: {time:.2f} sekund",
        "run_test": "Stiskněte 1 pro spuštění CPU testu",
        "generate_graph": "Stiskněte 2 pro vygenerování grafu z uložených dat",
        "invalid_input": "Neplatný vstup, ukončuji.",
        "installing_pyspectator": "Instaluji pyspectator pro Windows...",
        "installing_lm_sensors": "Instaluji lm-sensors pro Linux...",
        "results_saved": "Výsledky uloženy do {filename}",
        "no_test_data": "Nejsou k dispozici žádná testovací data.",
        "unsupported_os": "Nepodporovaný operační systém.",
        "graph_title": "Výsledky CPU benchmarku",
        "graph_xlabel": "Časové razítko",
        "graph_ylabel": "Doba testu (s)",
        "enter_duration": "Zadejte dobu trvání testu v sekundách (výchozí je 20): ",
        "installing_pyspectator_excuse": "Omlouvám se, ale moje zkušenosti z vyčítáním teplot pro windows nejsou dobré tak to tu zatím nebude.",
        "display_or_export": "Chcete zobrazit graf v okně (1) nebo jej exportovat do obrazového souboru (2)? ",
        "export_format": "Zadejte požadovaný formát exportu (png, svg, jpeg, atd.): ",
        "export_success": "Graf úspěšně exportován do {filename}",
        "export_failed": "Export grafu selhal.",
        "invalid_export_format": "Neplatný formát exportu.",
        "display_failed": "Nepodařilo se zobrazit graf. Exportuji do SVG.",
        "latest_version": "Nejnovější dostupná verze: {version}",
        "check_updates": "Zkontrolujte aktualizace na: {url}",
        "update_failed": "Nepodařilo se zkontrolovat aktualizace.",
        "connection_error": "Nepodařilo se připojit k GitHubu pro kontrolu aktualizací.",
    }
}

class Colors:
    RED = "\033[91m"
    RESET = "\033[0m"

def cpu_stress():
    while True:
        pass

def get_cpu_info():
    info = cpuinfo.get_cpu_info()
    cpu_name = info['brand_raw'] if 'brand_raw' in info else 'Unknown'
    cores = psutil.cpu_count(logical=False)
    threads = psutil.cpu_count(logical=True)
    freq = psutil.cpu_freq()
    return {
        "CPU Name": cpu_name,
        "Physical Cores": cores,
        "Logical Threads": threads,
        "Max Frequency": f"{freq.max:.2f} MHz" if freq else "Unknown"
    }

def get_cpu_temps():
    system = platform.system()
    if system == "Windows":
        return locales[LANG]["temp_not_available"]
    elif system == "Linux":
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                return {sensor.label or f"Core {i}": temp.current for i, sensor in enumerate(temps['coretemp'])}
            return locales[LANG]["temp_not_available"]
        except AttributeError:
            return locales[LANG]["temp_not_available"]
    else:
        return locales[LANG]["temp_not_available"]

def save_results(cpu_info, temps, duration):
    os.makedirs("completed_tests", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    filename = f"completed_tests/{cpu_info['CPU Name']}_{timestamp}.json"
    data = {
        "cpu_info": cpu_info,
        "temps": temps,
        "duration": duration
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(locales[LANG]["results_saved"].format(filename=filename))

def generate_graph():
    files = os.listdir("completed_tests")
    if not files:
        print(locales[LANG]["no_test_data"])
        return
    
    durations = []
    timestamps = []
    
    for file in sorted(files):
        with open(f"completed_tests/{file}", "r") as f:
            data = json.load(f)
            durations.append(data["duration"])
            timestamps.append(file.replace(".json", ""))
    
    plt.figure(figsize=(12, 6))
    plt.plot(timestamps, durations, marker='o')
    plt.xlabel(locales[LANG]["graph_xlabel"])
    plt.ylabel(locales[LANG]["graph_ylabel"])
    plt.title(locales[LANG]["graph_title"])
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.grid()
    
    choice = input(locales[LANG]["display_or_export"])
    
    if choice == "1":
        try:
            plt.show()
        except Exception as e:
            print(f"{Colors.RED}{locales[LANG]['display_failed']}{Colors.RESET}")
            export_graph("svg")
    elif choice == "2":
        export_format = input(locales[LANG]["export_format"]).strip().lower()
        if export_format in ["png", "svg", "jpeg", "jpg", "pdf"]:
            export_graph(export_format)
        else:
            print(locales[LANG]["invalid_export_format"])
    else:
        print(locales[LANG]["invalid_input"])

def export_graph(format):
    os.makedirs("exports", exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M")
    filename = f"exports/graph_{timestamp}.{format}"
    try:
        plt.savefig(filename, format=format, bbox_inches='tight')
        print(locales[LANG]["export_success"].format(filename=filename))
    except Exception as e:
        print(f"{Colors.RED}{locales[LANG]['export_failed']}{Colors.RESET}")

def install_required_tools():
    system = platform.system()
    if system == "Windows":
        # print(locales[LANG]["installing_pyspectator"])
        print(locales[LANG]["installing_pyspectator_excuse"])
        # subprocess.run(["pip", "install", "pyspectator"], check=True)
    elif system == "Linux":
        print(locales[LANG]["installing_lm_sensors"])
        subprocess.run(["sudo", "apt-get", "install", "lm-sensors"], check=True)
        subprocess.run(["sudo", "sensors-detect"], check=True)
    else:
        print(locales[LANG]["unsupported_os"])

def main():
    print(locales[LANG]["run_test"])
    print(locales[LANG]["generate_graph"])
    choice = input("Select an option (1-2): ")
    
    if choice == "1":
        duration_input = input(locales[LANG]["enter_duration"])
        try:
            duration = int(duration_input) if duration_input else 20
        except ValueError:
            print(locales[LANG]["invalid_input"])
            return
        
        print(locales[LANG]["starting_benchmark"])
        start_time = time.time()
        
        processes = []
        for _ in range(psutil.cpu_count(logical=True)):
            p = multiprocessing.Process(target=cpu_stress)
            p.start()
            processes.append(p)
        
        time.sleep(duration)
        
        for p in processes:
            p.terminate()
            p.join()
        
        end_time = time.time()
        print(locales[LANG]["benchmark_completed"])
        
        print(locales[LANG]["cpu_info"])
        cpu_info = get_cpu_info()
        for key, value in cpu_info.items():
            print(f"{key}: {value}")
        
        print(locales[LANG]["cpu_temperatures"])
        temps = get_cpu_temps()
        if isinstance(temps, dict):
            for key, value in temps.items():
                print(f"{key}: {value}°C")
        else:
            print(temps)
        
        duration = end_time - start_time
        print(locales[LANG]["test_duration"].format(time=duration))
        
        save_results(cpu_info, temps, duration)
    
    elif choice == "2":
        generate_graph()
    
    else:
        print(locales[LANG]["invalid_input"])

def check_for_updates():
    url = "https://api.github.com/repos/stepanvalic/CPU-benchmark/releases/latest"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            latest_version = response.json().get("tag_name", "Unknown")
            print(locales[LANG]["latest_version"].format(version=latest_version))
            print(locales[LANG]["check_updates"].format(url=url))
        else:
            print(f"{Colors.RED}{locales[LANG]['update_failed']}{Colors.RESET}")
    except requests.RequestException:
        print(locales[LANG]["connection_error"])

check_for_updates()

if __name__ == "__main__":
    install_required_tools()
    main()