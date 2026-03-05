import numpy as np
import matplotlib.pyplot as plt
import time

# Parametry
N = 1207
a1 = 10
a2 = -1
a3 = -1
tol = 1e-9
max_iter = 200

def create_matrix():
    A = np.zeros((N, N))
    np.fill_diagonal(A, a1)
    np.fill_diagonal(A[1:], a2)
    np.fill_diagonal(A[:,1:], a2)
    np.fill_diagonal(A[2:], a3)
    np.fill_diagonal(A[:,2:], a3)
    return A

def create_vector():
    # b[n] = sin((n+1)*10)
    return np.array([np.sin((n + 1) * 10) for n in range(N)]).reshape((N, 1))

def solve_jacobi(A, b):
    start = time.time()
    L = np.tril(A, -1)
    U = np.triu(A, 1)
    D = np.diag(np.diag(A))
    M = -np.linalg.solve(D, (L + U))
    w = np.linalg.solve(D, b)

    x = np.ones((N, 1))
    r_norm = []
    r = A @ x - b
    inorm = np.linalg.norm(r)
    r_norm.append(inorm)
    iteration_count = 0
    while inorm > tol and iteration_count < max_iter:
        x = M @ x + w
        r = A @ x - b
        inorm = np.linalg.norm(r)
        r_norm.append(inorm)
        iteration_count += 1

    time_c = (time.time() - start) * 1000
    return r_norm, iteration_count, round(time_c, 0)

def solve_gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    start = time.time()
    N = A.shape[0]
    x = np.ones((N, 1))  # początkowe przybliżenie

    # Rozkład A = T + U
    D = np.diag(np.diag(A))
    L = np.tril(A, -1)
    U = np.triu(A, 1)
    T = D + L

    r = A @ x - b
    r_norm = [np.linalg.norm(r)]
    iteration_count = 0

    for k in range(max_iter):
        rhs = b - U @ x  # wektor prawej strony
        x = np.linalg.solve(T, rhs)  # rozwiązujemy T * x = rhs

        r = A @ x - b
        norm_r = np.linalg.norm(r)
        r_norm.append(norm_r)
        iteration_count += 1

        if norm_r < tol:
            break

    time_c = (time.time() - start)*1000  # czas w milisekundach
    return r_norm, iteration_count, round(time_c, 0)


if __name__ == '__main__':
    A = create_matrix()
    b = create_vector()

    r_norm, ic_j, time_j = solve_jacobi(A, b)
    plt.semilogy(r_norm)

    r_norm, ic_gs, time_gs = solve_gauss_seidel(A, b)
    plt.semilogy(r_norm)
    plt.legend([f"Jacobi l. iteracji: {ic_j}, czas: {time_j} ms", f"Gauss-Seidel l. iteracji: {ic_gs}, czas: {time_gs} ms"])

    plt.grid(True)
    plt.xlabel("Iteracja")
    plt.ylabel("Norma residuum")
    plt.title("Metody iteracyjne")

    plt.show()



