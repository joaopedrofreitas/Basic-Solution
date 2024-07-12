import sys
import math

Viavel=0
Inviavel=0


def read_file(file):#OK!
    with open(file, 'r') as f:
        n, m = map(int, f.readline().split())
        c = [int(num) for num in f.readline().split()]
        A=[]
        for _ in range(m):
            A.append([int(num) for num in f.readline().split()])
        b = [int(num) for num in f.readline().split()]
    return n,m,c,A,b

def get_combinacoes(lista,tam):
    n = len(lista)
    indices = list(range(tam))
    result = []
    while True:
        result.append([lista[i] for i in indices])
        for i in reversed(range(tam)):
            if indices[i] != i + n - tam:
                break
        else:
            return result
        indices[i] += 1
        for j in range(i + 1, tam):
            indices[j] = indices[j - 1] + 1

def get_coluna(matriz, col_index):
    return [linha[col_index] for linha in matriz]

def set_coluna(matriz,values,col_index):
    for i in range(len(matriz)):
        matriz[i][col_index] = values[i]

def get_size_Matriz(matriz):
    linhas=len(matriz)
    colunas=len(matriz[0])
    return linhas,colunas

def print_matrix(matriz):
    for linha in matriz:
        print("[", end=" ")
        for elemento in linha:
            print(elemento, end=" ")
        print("]")

def Eliminacao_Gauss(A,b,I,O,num_lin):    
    n = len(A)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_el = abs(M[i][i])
        max_row = i
        for k in range(i+1, n):
            if abs(M[k][i]) > max_el:
                max_el = abs(M[k][i])
                max_row = k
        M[i], M[max_row] = M[max_row], M[i]

        if M[i][i] == 0:
            return None

        for k in range(i+1, n):
            c = -M[k][i] / M[i][i]
            for j in range(i, n+1):
                if i == j:
                    M[k][j] = 0
                else:
                    M[k][j] += c * M[i][j]

    x = [0 for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] / M[i][i]
        for k in range(i-1, -1, -1):
            M[k][n] -= M[k][i] * x[i]

    f = {chave: 0 for chave in range(num_lin)}                                #Salvar respostas em map{x1:Val, x2: Val, x3: Val, XN: Val }
    i=0
    for idx in I:
        f[idx]=x[i]
        i+=1
    return f

def is_viable(Solution):
    global Viavel
    global Inviavel
    for i in Solution.values():
        if i < 0:
            Inviavel+=1
            return False
    Viavel+=1
    return True   
 
def objective_func(Solution,c):
    i=0
    Resp=0
    for coeficiente in c:
        Resp+=coeficiente*Solution[i]
        i+=1
    return Resp

def solve(filename):
    n, m, c, A, b = read_file(filename)
    Combinacoes= get_combinacoes(list(range(n)),m)                                      #  Indices (x1,x2,x3,x4,x5 ... xN)            
    Solutions=[]                     
    for I in Combinacoes:
        A_B= [[0 for _ in range(m)] for _ in range(m)]                                  #  Matriz que será utilizada nos calculos
        aux=0
        for idx in I:                                                                   #  Montar a matriz A
            set_coluna(A_B,get_coluna(A,idx),aux)
            aux+=1
        Solutions.append(Eliminacao_Gauss(A_B,b,I,A,n))
    return Solutions,c
        
    

if __name__ ==  "__main__":
    filename = sys.argv[1]
    Solutions,c = solve(filename)
    for i in Solutions:
        z=0
        if i is not None:
            valores_x = ", ".join(str(i[j]) for j in range(len(i)))
            z=objective_func(i,c)
            print(f"Solução: x=({valores_x}), z={z} ,{'viável' if is_viable(i) else 'inviável'}")
    print(f"Soluções Básicas viaveis:\t {Viavel}")
    print(f"Soluções Básicas Inviaveis:\t {Inviavel}")
    