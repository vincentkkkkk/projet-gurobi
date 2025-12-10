from solver_gurobi import solve_exact, generate_solution_text

def main():
    # Si le fichier example.in est dans le même dossier que videos.py
    dataset_path = "example.in"

    # Résolution du modèle
    model, x, y, V, C = solve_exact(dataset_path)

    # Écrire le fichier MPS
    model.write("videos.mps")

    # Générer le fichier de solution
    solution_text = generate_solution_text(x, V, C)
    with open("videos.out", "w", encoding="utf-8") as f:
        f.write(solution_text)

    print("Solution générée avec succès !")

if __name__ == "__main__":
    main()
