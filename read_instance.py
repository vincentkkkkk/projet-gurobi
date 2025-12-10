def read_instance(filename):
    """Lit un fichier dataset et retourne toutes les données sous forme de listes et dictionnaires."""
    with open(filename, "r", encoding="utf-8") as f:
        data = [line.strip() for line in f]

    # 1. Première ligne
    V, E, R, C, X = map(int, data[0].split())

    # 2. Tailles des vidéos
    video_size = list(map(int, data[1].split()))

    # 3. Endpoints
    idx = 2
    LD = []                   # latence data center pour chaque endpoint
    connections = []          # liste de dictionnaires {cache_id: latency}
    for _ in range(E):
        ld, K = map(int, data[idx].split())
        idx += 1
        LD.append(ld)
        con = {}
        for _ in range(K):
            c, lc = map(int, data[idx].split())
            con[c] = lc
            idx += 1
        connections.append(con)

    # 4. Requêtes
    requests = []  # tuples (video_id, endpoint_id, n_requests)
    for _ in range(R):
        v, e, n = map(int, data[idx].split())
        requests.append((v, e, n))
        idx += 1

    return V, E, R, C, X, video_size, LD, connections, requests


# Test rapide
if __name__ == "__main__":
    instance = read_instance("example.in")
    print("Instance loaded successfully!")
    print(instance)
