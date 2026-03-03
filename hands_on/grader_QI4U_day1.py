from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import numpy as np

def ex_1(qc):
    qc1 = QuantumCircuit(1)
    qc1.h(0)
    qc1.x(0)
    qc1.h(0)

    # ゲートの構成が完全に一致しているかを判定
    if qc == qc1:
        return "Correct!!"
    else:
        return "Wrong answer, try again!"
    
def ex_2(qc):
    qc2 = QuantumCircuit(1)
    qc2.x(0)

    # ゲートの構成が完全に一致しているかを判定
    if qc == qc2:
        return "Correct!!"
    else:
        return "Wrong answer, try again!"

def ex_3(qc):
    qc3 = QuantumCircuit(1)
    qc3.h(0)

    state1 = Statevector.from_instruction(qc3)
    state2 = Statevector.from_instruction(qc)

    # 振幅の絶対値の2乗（観測確率）を計算
    probs1 = np.abs(state1.data)**2
    probs2 = np.abs(state2.data)**2

    # np.allcloseで、全ての状態の確率が一致しているかを判定
    if np.allclose(probs1, probs2):
        return "Correct!!"
    else:
        return "Wrong answer, try again!"
    
def ex_4(qc):
    qc4 = QuantumCircuit(2)
    qc4.h(0)
    qc4.h(1)

    state1 = Statevector.from_instruction(qc4)
    state2 = Statevector.from_instruction(qc)

    if np.isclose(np.abs(state1.inner(state2)), 1.0):
        return "Correct!!"
    else:
        return "Wrong answer, try again!"
    
def ex_5(qc):
    qc5 = QuantumCircuit(2)
    qc5.h(0)
    qc5.cx(0, 1)

    state1 = Statevector.from_instruction(qc5)
    state2 = Statevector.from_instruction(qc)

    if np.isclose(np.abs(state1.inner(state2)), 1.0):
        return "Correct!!"
    else:
        return "Wrong answer, try again!"