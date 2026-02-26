import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector


#量子状態をサークル記法で描画する関数(描写する際, グローバル位相の削除も自動で行う)
def plot_circle_notation(quantum_data, cols=4):

    # --- 1. データ抽出 ---
    if isinstance(quantum_data, QuantumCircuit):
        state = Statevector.from_instruction(quantum_data).data
    elif hasattr(quantum_data, "data"):
        state = quantum_data.data
    else:
        state = np.array(quantum_data)

    # --- グローバル位相の除去 ---
    first_nonzero_index = -1
    for i in range(len(state)):
        if np.abs(state[i]) > 0.00001:
            first_nonzero_index = i
            break
    if first_nonzero_index != -1:
        base_phase = np.angle(state[first_nonzero_index])
        state = state * np.exp(-1j * base_phase)

    n_states = len(state)
    n_qubits = int(np.log2(n_states))

    # --- 2. グリッド設定 ---
    grid_cols = min(n_states, cols)
    grid_rows = int(np.ceil(n_states / grid_cols))

    R = 0.5
    spacing_x = 2.5 * R
    spacing_y = 4.0 * R
    figsize = (grid_cols * 2.0, grid_rows * 2.2)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect('equal')
    ax.axis('off')

    # --- 3. 描画ループ ---
    for i in range(n_states):
        row = i // grid_cols
        col = i % grid_cols

        x0 = col * spacing_x
        y0 = (grid_rows - 1 - row) * spacing_y

        amp = state[i]
        prob_radius = np.abs(amp) * R
        phase_rad = np.angle(amp)

        # 外枠
        circle_frame = plt.Circle((x0, y0), R, edgecolor='black', facecolor='white', lw=1.5, zorder=1)
        ax.add_patch(circle_frame)

        # 塗りつぶし
        if prob_radius > 0.001:
            circle_fill = plt.Circle((x0, y0), prob_radius, color='cornflowerblue', zorder=2)
            ax.add_patch(circle_fill)

        # 棒 (位相)
        if np.abs(amp) > 0.0001:
            arrow_length = R
            x_end = x0 + arrow_length * np.sin(phase_rad)
            y_end = y0 + arrow_length * np.cos(phase_rad)
            ax.plot([x0, x_end], [y0, y_end], color='black', lw=2, zorder=3)

        # ラベル
        if n_states == 2:
            label_text = f"|{i}⟩"
        else:
            label_bin = format(i, f'0{n_qubits}b')
            label_text = f"|{label_bin}⟩"

        ax.text(x0, y0 - R - 0.3, label_text, color='black', fontsize=12, ha='center', va='top')

    margin_x = R + 0.5
    margin_y = R + 0.5
    ax.set_xlim(-margin_x, (grid_cols-1)*spacing_x + margin_x)
    ax.set_ylim(-margin_y, (grid_rows-1)*spacing_y + margin_y)

    plt.tight_layout()
    plt.show()


#==========================================
#初期状態と量子回路を受け取り、結果を描画・出力する関数(circle notation, statevectorのon offを選べる)
#5qubits状態あたりまでスムーズに動作する
from qiskit.quantum_info import Statevector

def simulate_and_plot(initial_state, qc, cols=4, show_plot=True, return_state=True):
    # 1. 初期状態をStatevectorに変換
    if isinstance(initial_state, str):
        sv_init = Statevector.from_label(initial_state)
    else:
        sv_init = Statevector(initial_state)

    # 2. 量子回路を適用して最終状態を計算
    sv_final = sv_init.evolve(qc)

    # 3. サークル記法の描画
    if show_plot:
        # plot_circle_notation が未定義の場合を考慮
        try:
            plot_circle_notation(sv_final, cols=cols)
        except NameError:
            print("エラー: plot_circle_notation 関数が定義されていません。")
            print("代わりに標準の描画（qsphere）を試みます。")
            from qiskit.visualization import plot_state_qsphere
            display(plot_state_qsphere(sv_final))

    if return_state:
        return sv_final
    else:
        return None

#==========================================
# 1qubitのcircle notation半径, 位相を指定して作図する関数.
def plot_qubit1(
    rQuantum0=1.0, rQuantum1=0.0, angle0=0, angle1=0,
    show_plot=True, return_state=True
):
    """
    量子ビットの図を描画し、状態ベクトルを出力する関数

    Parameters:
    -----------
    show_plot : bool
        サークル記法の図を描画するかどうか
    show_text : bool
        Quantum State（状態ベクトル）をテキスト出力するかどうか
    """

    # 1. Quantum State の計算 ( r * e^(i * theta) )
    amp0 = rQuantum0 * np.exp(1j * np.radians(angle0))
    amp1 = rQuantum1 * np.exp(1j * np.radians(angle1))
    state_vector = np.array([amp0, amp1])



    # 3. 図の描画 (show_plot=Trueのとき)
    if show_plot:
        gap=2
        R=0.7
        figsize=(4,2)

        r0 = R * rQuantum0
        r1 = R * rQuantum1

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_aspect('equal')
        ax.axis('off')

        fill_color = 'cornflowerblue'

        # |0⟩
        circle0 = plt.Circle((0,0), R, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(circle0)
        if r0 > 0:
            inner0 = plt.Circle((0,0), r0, color=fill_color)
            ax.add_patch(inner0)
            angle0_rad = np.radians(angle0)
            x_end0 = 0 + R * np.sin(angle0_rad)
            y_end0 = 0 + R * np.cos(angle0_rad)
            ax.plot([0, x_end0], [0, y_end0], color='black', lw=2)
        ax.text(0, -R-0.15, "|0⟩", color='black', fontsize=12, ha='center', va='top')

        # |1⟩
        circle1 = plt.Circle((gap,0), R, edgecolor='black', facecolor='none', lw=2)
        ax.add_patch(circle1)
        if r1 > 0:
            inner1 = plt.Circle((gap,0), r1, color=fill_color)
            ax.add_patch(inner1)
            angle1_rad = np.radians(angle1)
            x_end1 = gap + R * np.sin(angle1_rad)
            y_end1 = 0 + R * np.cos(angle1_rad)
            ax.plot([gap, x_end1], [0, y_end1], color='black', lw=2)
        ax.text(gap, -R-0.15, "|1⟩", color='black', fontsize=12, ha='center', va='top')

        ax.set_xlim(-1, gap+1)
        ax.set_ylim(-1, R+0.5)
        plt.show()

    if return_state:
        return state_vector
    else:
        return None

#==========================================
# 2qubitのcircle notation半径, 位相を指定して作図する関数.
def plot_qubit2(
    rQuantum00=1.0, rQuantum01=0.0, rQuantum10=0.0, rQuantum11=0.0,
    angle00=0, angle01=0, angle10=0, angle11=0,
    show_plot=True, return_state=True):
    """
    2量子ビットの状態を2x2グリッドで描画し、状態ベクトルを出力する
    """

    # 1. Quantum State の計算
    amp00 = rQuantum00 * np.exp(1j * np.radians(angle00))
    amp01 = rQuantum01 * np.exp(1j * np.radians(angle01))
    amp10 = rQuantum10 * np.exp(1j * np.radians(angle10))
    amp11 = rQuantum11 * np.exp(1j * np.radians(angle11))
    state_vector = np.array([amp00, amp01, amp10, amp11])

    # 3. 図の描画
    if show_plot:
        R=0.7
        gap=2
        figsize=(4,6)

        states = [
            {"r": rQuantum00, "angle": angle00, "label":"00", "pos": (0, gap)},
            {"r": rQuantum01, "angle": angle01, "label":"01", "pos": (gap, gap)},
            {"r": rQuantum10, "angle": angle10, "label":"10", "pos": (0, 0)},
            {"r": rQuantum11, "angle": angle11, "label":"11", "pos": (gap, 0)},
        ]

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_aspect('equal')
        ax.axis('off')

        fill_color = "cornflowerblue"

        for i, state in enumerate(states):
            x0, y0 = state["pos"]
            r = R * state["r"]

            # 外円
            circle = plt.Circle((x0, y0), R, edgecolor='black', facecolor='none', lw=2, zorder=1)
            ax.add_patch(circle)

            # 内円
            if r > 0:
                inner = plt.Circle((x0, y0), r, color=fill_color, zorder=2)
                ax.add_patch(inner)

                # 棒
                angle_rad = np.radians(state["angle"])
                x_end = x0 + R * np.sin(angle_rad)
                y_end = y0 + R * np.cos(angle_rad)
                ax.plot([x0, x_end], [y0, y_end], color='black', lw=2, zorder=3)

            # ラベル
            ax.text(x0, y0-R-0.15, f"|{state['label']}⟩", color='black', fontsize=12, ha='center', va='top')

        ax.set_xlim(-1, gap+R+1)
        ax.set_ylim(-1, gap+R+1)
        plt.show()

    if return_state:
        return state_vector
    else:
        return None

#==========================================
# 3qubitのcircle notation半径, 位相を指定して作図する関数.
def plot_qubit3(
    rQuantum000=1.0, rQuantum001=0.0, rQuantum010=0.0, rQuantum011=0.0,
    rQuantum100=0.0, rQuantum101=0.0, rQuantum110=0.0, rQuantum111=0.0,
    angle000=0, angle001=0, angle010=0, angle011=0,
    angle100=0, angle101=0, angle110=0, angle111=0,
    show_plot=True, return_state=True
):
    """
    3量子ビットの状態を2行4列のグリッドで描画し、状態ベクトルを出力する

    Parameters
    ----------
    show_plot : bool
        サークル記法の図を描画するかどうか
    show_text : bool
        Quantum State（状態ベクトル）をテキスト出力するかどうか
    """

    # 1. Quantum State の計算 ( r * e^(i * theta) )
    amp000 = rQuantum000 * np.exp(1j * np.radians(angle000))
    amp001 = rQuantum001 * np.exp(1j * np.radians(angle001))
    amp010 = rQuantum010 * np.exp(1j * np.radians(angle010))
    amp011 = rQuantum011 * np.exp(1j * np.radians(angle011))
    amp100 = rQuantum100 * np.exp(1j * np.radians(angle100))
    amp101 = rQuantum101 * np.exp(1j * np.radians(angle101))
    amp110 = rQuantum110 * np.exp(1j * np.radians(angle110))
    amp111 = rQuantum111 * np.exp(1j * np.radians(angle111))

    # 8つの状態を持つ配列を作成
    state_vector = np.array([
        amp000, amp001, amp010, amp011,
        amp100, amp101, amp110, amp111
    ])



    # 3. 図の描画 (show_plot=Trueのとき)
    if show_plot:
        R = 0.7
        gap = 2
        figsize = (8, 4) # 4列×2行に合わせて横長に調整

        # 8つの状態のパラメータと座標（2行×4列）を定義
        states = [
            {"r": rQuantum000, "angle": angle000, "label":"000", "pos": (0,       gap)},
            {"r": rQuantum001, "angle": angle001, "label":"001", "pos": (gap,     gap)},
            {"r": rQuantum010, "angle": angle010, "label":"010", "pos": (2 * gap, gap)},
            {"r": rQuantum011, "angle": angle011, "label":"011", "pos": (3 * gap, gap)},
            {"r": rQuantum100, "angle": angle100, "label":"100", "pos": (0,       0)},
            {"r": rQuantum101, "angle": angle101, "label":"101", "pos": (gap,     0)},
            {"r": rQuantum110, "angle": angle110, "label":"110", "pos": (2 * gap, 0)},
            {"r": rQuantum111, "angle": angle111, "label":"111", "pos": (3 * gap, 0)},
        ]

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_aspect('equal')
        ax.axis('off')
        # 背景を白（デフォルト）に戻しました

        # 8つの状態に割り当てる色（全て同じ色に統一）
        colors = ["cornflowerblue"] * 8  # 例: cornflowerblue

        for i, state in enumerate(states):
            x0, y0 = state["pos"]
            r = R * state["r"]

            # 外円（枠線を黒、中を白に修正）
            circle = plt.Circle((x0, y0), R, edgecolor='black', facecolor='white', lw=1.5, zorder=1)
            ax.add_patch(circle)

            # 内円と棒
            if r > 0.001:
                # 塗りつぶし円
                inner = plt.Circle((x0, y0), r, color=colors[i], zorder=2)
                ax.add_patch(inner)

                # 棒 (位相) ※長さは外円(R)と同じに固定
                angle_rad = np.radians(state["angle"])
                x_end = x0 + R * np.sin(angle_rad)
                y_end = y0 + R * np.cos(angle_rad)
                ax.plot([x0, x_end], [y0, y_end], color='black', lw=2, zorder=3)

            # ラベル（文字色を黒に修正）
            ax.text(x0, y0 - R - 0.2, f"|{state['label']}⟩", color='black', fontsize=12, ha='center', va='top')

        # 表示範囲の調整
        ax.set_xlim(-1, 3 * gap + R + 1)
        ax.set_ylim(-1, gap + R + 1)

        # 余白を自動調整して表示
        plt.tight_layout()
        plt.show()

# 最後の return 部分を条件分岐にする
    if return_state:
        return state_vector
    else:
        return None


#=====================================
#サンプリング結果を受け取ってグラフ化する関数
def plot_sampling_histogram(counts, title="Sampling Result"):
    """
    サンプリング結果の辞書を受け取り、すべての基底状態(0...0 ~ 1...1)を含む棒グラフを描画する関数
    (既存のコードそのまま)
    """
    sample_key = list(counts.keys())[0]
    n_qubits = len(sample_key)
    n_states = 2 ** n_qubits

    all_labels = [format(i, f'0{n_qubits}b') for i in range(n_states)]
    frequencies = [counts.get(label, 0) for label in all_labels]

    width = max(8, n_states * 0.4)
    fig, ax = plt.subplots(figsize=(width, 4))

    bars = ax.bar(all_labels, frequencies, color='cornflowerblue', edgecolor='black')

    ax.set_xlabel('Measurement Outcomes', fontsize=12)
    ax.set_ylabel('Counts', fontsize=12)
    ax.set_title(f'{title} ({n_qubits} qubits)', fontsize=14)

    plt.xticks(rotation=90, fontsize=10)

    max_freq = max(frequencies) if frequencies else 1
    ax.set_ylim(0, max_freq * 1.2)

    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10)

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

#状態を受け取ってサンプリング＆グラフ化する関数
def sample_and_plot_histogram(state_data, shots=1000, title="Sampling Result"):
    """
    量子状態を受け取り、有限回サンプリングして結果をグラフ化する関数

    Parameters:
    -----------
    state_data : list, np.array, Statevector, or QuantumCircuit
        サンプリング対象の量子状態
    shots : int
        サンプリング（測定）を行う回数（デフォルト: 1000回）
    title : str
        グラフのタイトル

    Returns:
    --------
    dict
        サンプリング結果の辞書 (例: {'000': 505, '111': 495})
    """
    # 1. 入力データを Qiskit の Statevector オブジェクトに変換
    if isinstance(state_data, QuantumCircuit):
        sv = Statevector.from_instruction(state_data)
    elif isinstance(state_data, Statevector):  # <--- ここを修正しました
        sv = state_data
    else:
        # リストやNumpy配列の場合
        sv = Statevector(state_data)

    # 2. Qiskitの機能を使ってサンプリングを実行
    counts = sv.sample_counts(shots=shots)



    # 4. グラフを描画
    plot_sampling_histogram(counts, title=f"{title} - {shots} shots")

    # 辞書データを返す（後で別の用途に使えるように）
    return None