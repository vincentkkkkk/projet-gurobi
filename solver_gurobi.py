from gurobipy import Model, GRB
from read_instance import read_instance

def solve_exact(filename):
    """Résout le problème avec Gurobi et renvoie le modèle et les variables."""
    # -----------------------------
    # Lecture des données
    # -----------------------------
    V, E, R, C, X, video_size, LD, connections, requests = read_instance(filename)

    # -----------------------------
    # Création du modèle
    # -----------------------------
    model = Model("HashCodeExact")
    model.Params.OutputFlag = 1  # affiche les traces
    model.Params.MIPGap = 5e-3   # 0.5% gap max

    # Variables binaires
    x = model.addVars(V, C, vtype=GRB.BINARY, name="x")  # vidéo v dans cache c
    y = model.addVars(R, C, vtype=GRB.BINARY, name="y")  # requête r servie par cache c

    # -----------------------------
    # Fonction objective
    # -----------------------------
    obj = 0
    for r, (v, e, n) in enumerate(requests):
        for c in range(C):
            if c in connections[e]:
                dc_lat = LD[e]
                cache_lat = connections[e][c]
                saving = (dc_lat - cache_lat) * n
                if saving > 0:
                    obj += saving * y[r, c]

    model.setObjective(obj, GRB.MAXIMIZE)

    # -----------------------------
    # Contraintes
    # -----------------------------
    # 1. Une seule cache au plus par requête
    for r in range(R):
        model.addConstr(sum(y[r, c] for c in range(C)) <= 1)

    # 2. Couplage y[r,c] ≤ x[v,c]
    for r, (v, e, n) in enumerate(requests):
        for c in range(C):
            model.addConstr(y[r, c] <= x[v, c])

    # 3. Capacité des caches
    for c in range(C):
        model.addConstr(sum(video_size[v] * x[v, c] for v in range(V)) <= X)

    # 4. y[r,c] = 0 si cache non connecté
    for r, (v, e, n) in enumerate(requests):
        for c in range(C):
            if c not in connections[e]:
                model.addConstr(y[r, c] == 0)

    # -----------------------------
    # Résolution
    # -----------------------------
    model.optimize()

    print("\nOptimal objective =", model.objVal)
    return model, x, y, V, C


def generate_solution_text(x, V, C):
    """Génère le texte du fichier videos.out à partir des variables x."""
    lines = []
    caches_used = []
    for c in range(C):
        videos_in_cache = [str(v) for v in range(V) if x[v, c].X > 0.5]
        if videos_in_cache:
            caches_used.append(f"{c} {' '.join(videos_in_cache)}")
    lines.append(str(len(caches_used)))
    lines.extend(caches_used)
    return "\n".join(lines)
