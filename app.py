import streamlit as st
import time

# --- N-Queens Solver with tracking ---
def solve_n_queens(n):
    board = [-1] * n
    solutions = []

    def is_safe(row, col):
        for r in range(row):
            if board[r] == col or abs(board[r] - col) == abs(r - row):
                return False
        return True

    def solve(row):
        if row == n:
            solutions.append(board.copy())
            return
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                solve(row + 1)
                board[row] = -1

    solve(0)
    return solutions

# --- Render HTML Chess Board ---
def render_html_board(board):
    n = len(board)
    html = '<div style="display: flex; justify-content: center;">'
    html += '<table style="border-collapse: collapse;">'
    for r in range(n):
        html += "<tr>"
        for c in range(n):
            is_queen = board[r] == c
            bg = "#f0d9b5" if (r + c) % 2 == 0 else "#b58863"
            html += f'<td style="width:50px;height:50px;text-align:center;font-size:28px;background:{bg};color:black;">{"♛" if is_queen else ""}</td>'
        html += "</tr>"
    html += "</table></div>"
    return html

# --- Backtracking animation with pause/play ---
def animate_solution(n, speed, placeholder, pause_flag):
    board = [-1] * n

    def is_safe(row, col):
        for r in range(row):
            if board[r] == col or abs(board[r] - col) == abs(r - row):
                return False
        return True

    def wait(duration):
        while st.session_state[pause_flag]:
            time.sleep(0.1)
        time.sleep(duration)

    def solve(row):
        if row == n:
            return True
        for col in range(n):
            if is_safe(row, col):
                board[row] = col
                placeholder.markdown(render_html_board(board), unsafe_allow_html=True)
                wait(speed)
                if solve(row + 1):
                    return True
                # backtrack
                board[row] = -1
                placeholder.markdown(render_html_board(board), unsafe_allow_html=True)
                wait(speed)
        return False

    solve(0)

# --- Main App ---
def main():
    st.set_page_config("♛ N-Queens Solver", layout="centered")
    st.markdown("<h1 style='text-align:center;'>♛ N-Queens Solver Dashboard</h1>", unsafe_allow_html=True)
    st.write("Visualize N-Queens backtracking step-by-step with optional animation.")

    n = st.slider("Select N (Board Size)", 4, 12, 8)
    animate = st.checkbox("Animate solving the first solution (works best for N ≤ 8)")
    speed = st.slider("Animation Speed (seconds):", 0.1, 15.0, 0.4)

    if "paused" not in st.session_state:
        st.session_state.paused = False
    if "animate_started" not in st.session_state:
        st.session_state.animate_started = False

    solve_btn = st.button("🔍 Solve N-Queens")

    if solve_btn:
        st.session_state.animate_started = False
        solutions = solve_n_queens(n)
        st.session_state.solutions = solutions
        st.session_state.n = n  # store n for later reference
        st.success(f"✅ Found {len(solutions)} solutions for {n}-Queens.")

        # Animate
        if animate and n <= 8:
            st.subheader("🎬 Animating First Solution with Backtracking")
            st.session_state.animate_started = True
            placeholder = st.empty()

            col1, col2 = st.columns(2)
            with col1:
                if st.button("⏸ Pause", key="pause_btn"):
                    st.session_state.paused = True
            with col2:
                if st.button("▶ Play", key="play_btn"):
                    st.session_state.paused = False

            animate_solution(n, speed, placeholder, "paused")

    # --- Solution Viewer Always Enabled if Available ---
    if "solutions" in st.session_state and st.session_state.solutions:
        solutions = st.session_state.solutions
        st.subheader("📘 View Specific Solution")
        st.markdown(f"Total Solutions: `{len(solutions)}`")
        selected = st.number_input("Enter solution number:", min_value=1, max_value=len(solutions), value=1, key="solution_selector")
        st.markdown(render_html_board(solutions[selected - 1]), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
