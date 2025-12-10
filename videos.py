import sys
from solver_gurobi import solve_exact, generate_solution_text

def main():
    if len(sys.argv) < 2:
        print("Usage: python videos.py <dataset_path>")
        sys.exit(1)

    dataset_path = sys.argv[1]
    print(f"Lecture du dataset : {dataset_path}")

    # Résolution du modèle exact avec Gurobi
    model, x, y, V, C = solve_exact(dataset_path)

    # S'assurer que le MIPGap est ≤ 0.5%
    model.Params.MIPGap = 5e-3

    # Montrer quelques informations pendant la résolution
    print("Construction du modèle terminée.")
    print(f"Nombre de variables binaires : {len(x) + len(y)}")
    print(f"Nombre de contraintes : {model.NumConstrs}")

    # Écrire le fichier MPS
    model.write("videos.mps")
    print("Fichier MPS généré : videos.mps")

    # Générer le fichier de solution
    solution_text = generate_solution_text(x, V, C)
    with open("videos.out", "w", encoding="utf-8") as f:
        f.write(solution_text)
    print("Fichier solution généré : videos.out")
    print("Solution générée avec succès !")

if __name__ == "__main__":
    main()
