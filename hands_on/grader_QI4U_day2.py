from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

def ex_1(qc):
    qc1 = QuantumCircuit(2)
    qc1.h(0)
    qc1.h(1)


    # ゲートの構成が完全に一致しているかを判定
    if qc == qc1:
        return "Correct!!"
    else:
        return "Wrong answer, try again!"
    
def ex_2(qc):
    qc2 = QuantumCircuit(2)
    qc2.h(1)
    qc2.cx(0,1)
    qc2.h(1)
    # ゲートの構成が完全に一致しているかを判定
    if qc == qc2:
        return "Correct!!"
    else:
        return "Wrong answer, try again!"

def ex_3(qc):
    qc3 = QuantumCircuit(2)
    qc3.h(0)
    qc3.h(1)
    qc3.x(0)
    qc3.x(1)
    qc3.h(1)
    qc3.cx(0,1)
    qc3.h(1)
    qc3.x(0)
    qc3.x(1)
    qc3.h(0)
    qc3.h(1)
    # ゲートの構成が完全に一致しているかを判定
    if qc == qc3:
        return "Correct!!"
    else:
        return "Wrong answer, try again!"