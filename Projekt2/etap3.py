import numpy as np
import matplotlib.pyplot as plt
import time
import math

# Parametry

a1 = 10
a2 = -1
a3 = -1
tol = 1e-9
max_iter = 1000

def create_matrix(N):
    A = np.zeros((N, N))
    np.fill_diagonal(A, a1)
    np.fill_diagonal(A[1:], a2)
    np.fill_diagonal(A[:,1:], a2)
    np.fill_diagonal(A[2:], a3)
    np.fill_diagonal(A[:,2:], a3)
    return A

def create_vector(N):
    # b[n] = sin((n+1)*10)
    return np.array([np.sin((n + 1) * 10) for n in range(N)]).reshape((N, 1))

def solve_jacobi(A, b):
    start = time.time()
    N=A.shape[0]
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

    time_c = (time.time() - start)
    return time_c


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

    time_c = (time.time() - start)
    return time_c

import numpy as np
import time

def lu_decomposition(A):
    N = A.shape[0]
    U = A.copy().astype(float)
    L = np.eye(N)

    for i in range(N):
        for j in range(i):
            if U[j, j] == 0:
                raise ValueError("Dzielenie przez zero – konieczne pivotowanie")
            L[i, j] = U[i, j] / U[j, j]
            U[i, :] -= L[i, j] * U[j, :]

    return L, U

def solve_direct(A, b):
    N = A.shape[0]
    t_start = time.time()

    L, U = lu_decomposition(A)

    # Rozwiązanie L * y = b
    y = np.linalg.solve(L, b)

    # Rozwiązanie U * x = y
    x = np.linalg.solve(U, y)

    r_norm = np.linalg.norm(A @ x - b)
    t_direct = (time.time() - t_start)

    return t_direct


if __name__ == '__main__':

    times_jacobi=[]
    times_gs=[]
    times_lu=[]
    x = [100, 500, 1000, 2000, 3000, 4000]
    for N in x:
        A = create_matrix(N)
        b = create_vector(N)
        times_lu.append(solve_direct(A, b))
        times_gs.append(solve_gauss_seidel(A, b))
        times_jacobi.append(solve_jacobi(A,b))

    plt.semilogy(x, times_jacobi)
    plt.semilogy(x, times_gs)
    plt.semilogy(x, times_lu)
    #plt.plot(x, times_jacobi)
    #plt.plot(x, times_gs)
    #plt.plot(x, times_lu)
    plt.legend([f" Jacobi ", f" Gauss-Seidel", f"Metoda LU"])

    plt.grid(True)
    plt.xlabel("N")
    plt.ylabel("Czas [s]")
    plt.title("Zależność czasu obliczeń od roziaru macierzy")

    plt.show()