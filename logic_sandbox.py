import pygame
import sys

# --- INITIALIZATION ---
print("Initializing Digital Logic Suite Pro...")
pygame.init()

WIDTH, HEIGHT = 1200, 800
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    print(f"Application Window Started.")
except pygame.error as e:
    print(f"Display Error: {e}")
    sys.exit()

pygame.display.set_caption("Logic Suite Pro | PS#08")
clock = pygame.time.Clock()

# --- THEME COLORS ---
BG = (10, 15, 25)
GRID = (25, 35, 50)
WIRE_OFF = (60, 75, 100)
WIRE_ON = (0, 230, 255)  # Neon Cyan
WIRE_CARRY = (57, 255, 20) # Neon Green
PANEL = (5, 10, 20)
ACCENT = (147, 51, 234) # Purple
TEXT = (240, 245, 255)

# --- FONTS ---
font_small = pygame.font.SysFont("Segoe UI", 14)
font_bold = pygame.font.SysFont("Segoe UI", 18, bold=True)
font_title = pygame.font.SysFont("Segoe UI", 28, bold=True)

class Gate:
    def __init__(self, x, y, type):
        self.rect = pygame.Rect(x, y, 110, 70)
        self.type = type
        self.inputs = [0, 0] if type != "NOT" else [0]
        self.output = 0
        self.input_conns = [None, None] if type != "NOT" else [None]
        self.dragging = False

    def update_logic(self):
        if self.type == "AND": self.output = 1 if all(self.inputs) else 0
        elif self.type == "OR": self.output = 1 if any(self.inputs) else 0
        elif self.type == "XOR": self.output = 1 if self.inputs[0] != self.inputs[1] else 0
        elif self.type == "NOT": self.output = 1 if self.inputs[0] == 0 else 0

    def draw(self, surf):
        color = WIRE_ON if self.output else WIRE_OFF
        # Glow effect
        if self.output:
            pygame.draw.rect(surf, (0, 50, 60), self.rect.inflate(4, 4), border_radius=10)
        
        pygame.draw.rect(surf, PANEL, self.rect, border_radius=10)
        pygame.draw.rect(surf, color, self.rect, 2, border_radius=10)
        
        txt = font_bold.render(self.type, True, TEXT)
        surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
        
        # Input Ports
        for i in range(len(self.inputs)):
            py = self.rect.y + (i + 1) * (self.rect.h / (len(self.inputs) + 1))
            pygame.draw.circle(surf, TEXT, (self.rect.x, int(py)), 6)
        
        # Output Port
        pygame.draw.circle(surf, color, (self.rect.right, self.rect.centery), 8)

class InputSource:
    def __init__(self, x, y, label=""):
        self.rect = pygame.Rect(x, y, 55, 55)
        self.state = 0
        self.dragging = False
        self.label = label

    def draw(self, surf):
        color = WIRE_ON if self.state else WIRE_OFF
        if self.state:
            pygame.draw.rect(surf, (0, 50, 60), self.rect.inflate(6, 6), border_radius=15)
        
        pygame.draw.rect(surf, color, self.rect, border_radius=15)
        txt = font_bold.render(str(self.state), True, PANEL)
        surf.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
        
        pygame.draw.circle(surf, color, (self.rect.right, self.rect.centery), 8)
        if self.label:
            lbl = font_small.render(self.label, True, TEXT)
            surf.blit(lbl, (self.rect.x, self.rect.y - 20))

def main():
    mode = "SIMULATOR"
    
    # Static Navigation Buttons
    btn_sim = pygame.Rect(20, 20, 180, 45)
    btn_snd = pygame.Rect(210, 20, 180, 45)

    # Designer Tools Buttons
    tool_and = pygame.Rect(40, HEIGHT-75, 90, 45)
    tool_or = pygame.Rect(140, HEIGHT-75, 90, 45)
    tool_xor = pygame.Rect(240, HEIGHT-75, 90, 45)
    tool_not = pygame.Rect(340, HEIGHT-75, 90, 45)
    tool_inp = pygame.Rect(440, HEIGHT-75, 110, 45)
    tool_clr = pygame.Rect(WIDTH-150, HEIGHT-75, 110, 45)

    # Data Structures
    sb_nodes = []
    sb_gates = []
    
    # Simulator Hardcoded Data
    sim_nodes = [InputSource(200, 250, "A"), InputSource(200, 450, "B")]
    sim_xor = Gate(500, 245, "XOR")
    sim_and = Gate(500, 445, "AND")

    temp_wire_start = None
    selected_obj = None

    while True:
        m_pos = pygame.mouse.get_pos()
        screen.fill(BG)
        
        # --- UI HEADER ---
        pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, 85))
        for btn, label, active in [(btn_sim, "SIMULATOR", mode == "SIMULATOR"), (btn_snd, "PRO DESIGNER", mode == "SANDBOX")]:
            color = WIRE_ON if active else WIRE_OFF
            pygame.draw.rect(screen, color, btn, border_radius=8)
            txt = font_bold.render(label, True, PANEL if active else TEXT)
            screen.blit(txt, (btn.centerx - txt.get_width()//2, btn.centery - txt.get_height()//2))

        # TEAM LABEL
        team_txt = font_small.render("Methodology PS#08 | MJ Devesh, Amitabh J, Mrithula JP", True, (100, 120, 150))
        screen.blit(team_txt, (WIDTH - team_txt.get_width() - 25, 33))

        if mode == "SIMULATOR":
            # Simulator Logic
            sim_xor.inputs = [sim_nodes[0].state, sim_nodes[1].state]
            sim_and.inputs = [sim_nodes[0].state, sim_nodes[1].state]
            sim_xor.update_logic()
            sim_and.update_logic()

            # Static Flow Lines
            pygame.draw.line(screen, WIRE_ON if sim_nodes[0].state else WIRE_OFF, (255, 277), (500, 265), 4)
            pygame.draw.line(screen, WIRE_ON if sim_nodes[0].state else WIRE_OFF, (255, 277), (500, 465), 4)
            pygame.draw.line(screen, WIRE_ON if sim_nodes[1].state else WIRE_OFF, (255, 477), (500, 295), 4)
            pygame.draw.line(screen, WIRE_ON if sim_nodes[1].state else WIRE_OFF, (255, 477), (500, 495), 4)
            
            for n in sim_nodes: n.draw(screen)
            sim_xor.draw(screen)
            sim_and.draw(screen)

            screen.blit(font_title.render("LOGIC STATE: HALF-ADDER", True, TEXT), (WIDTH//2 - 170, 140))
            screen.blit(font_bold.render(f"SUM BIT: {sim_xor.output}", True, WIRE_ON if sim_xor.output else TEXT), (630, 268))
            screen.blit(font_bold.render(f"CARRY BIT: {sim_and.output}", True, WIRE_CARRY if sim_and.output else TEXT), (630, 468))

        else: # DESIGNER MODE
            # Grid
            for x in range(0, WIDTH, 50): pygame.draw.line(screen, GRID, (x, 85), (x, HEIGHT-85))
            for y in range(85, HEIGHT, 50): pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

            # Bottom Toolbar
            pygame.draw.rect(screen, PANEL, (0, HEIGHT-85, WIDTH, 85))
            tools = [(tool_and, "AND", WIRE_OFF), (tool_or, "OR", WIRE_OFF), 
                     (tool_xor, "XOR", WIRE_OFF), (tool_not, "NOT", WIRE_OFF), 
                     (tool_inp, "+ INPUT", ACCENT), (tool_clr, "CLEAR", (220, 50, 50))]
            
            for b, l, c in tools:
                pygame.draw.rect(screen, c, b, border_radius=6)
                t = font_bold.render(l, True, TEXT)
                screen.blit(t, (b.centerx - t.get_width()//2, b.centery - t.get_height()//2))

            # Designer Logic
            for g in sb_gates:
                for i in range(len(g.inputs)):
                    conn = g.input_conns[i]
                    g.inputs[i] = (conn.output if hasattr(conn, 'output') else conn.state) if conn else 0
                g.update_logic()

            # Designer Wires
            for g in sb_gates:
                for i, conn in enumerate(g.input_conns):
                    if conn:
                        color = WIRE_ON if (hasattr(conn, 'output') and conn.output) or (hasattr(conn, 'state') and conn.state) else WIRE_OFF
                        pygame.draw.line(screen, color, (conn.rect.right, conn.rect.centery), (g.rect.left, g.rect.y + (i + 1) * (g.rect.h / (len(g.inputs) + 1))), 4)

            if temp_wire_start: pygame.draw.line(screen, WIRE_ON, temp_wire_start, m_pos, 2)
            for n in sb_nodes: n.draw(screen)
            for g in sb_gates: g.draw(screen)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_sim.collidepoint(m_pos): mode = "SIMULATOR"
                if btn_snd.collidepoint(m_pos): mode = "SANDBOX"

                if mode == "SIMULATOR":
                    for n in sim_nodes:
                        if n.rect.collidepoint(m_pos): n.state = 1 - n.state
                else:
                    # Designer Tool Logic
                    if tool_and.collidepoint(m_pos): sb_gates.append(Gate(WIDTH//2, HEIGHT//2, "AND"))
                    if tool_or.collidepoint(m_pos): sb_gates.append(Gate(WIDTH//2, HEIGHT//2, "OR"))
                    if tool_xor.collidepoint(m_pos): sb_gates.append(Gate(WIDTH//2, HEIGHT//2, "XOR"))
                    if tool_not.collidepoint(m_pos): sb_gates.append(Gate(WIDTH//2, HEIGHT//2, "NOT"))
                    if tool_inp.collidepoint(m_pos): sb_nodes.append(InputSource(100, 300))
                    if tool_clr.collidepoint(m_pos): sb_nodes, sb_gates = [], []

                    for n in sb_nodes:
                        if n.rect.collidepoint(m_pos): n.state = 1 - n.state
                    
                    for obj in sb_nodes + sb_gates:
                        if obj.rect.collidepoint(m_pos):
                            # Check for wire output port (right side)
                            port_rect = pygame.Rect(obj.rect.right-15, obj.rect.centery-20, 35, 40)
                            if port_rect.collidepoint(m_pos):
                                temp_wire_start = (obj.rect.right, obj.rect.centery)
                                selected_obj = obj
                            else:
                                obj.dragging = True
                                selected_obj = obj

            if event.type == pygame.MOUSEBUTTONUP:
                if mode == "SANDBOX":
                    if temp_wire_start:
                        for g in sb_gates:
                            for i in range(len(g.inputs)):
                                in_port_rect = pygame.Rect(g.rect.left-20, g.rect.y + (i + 1) * (g.rect.h / (len(g.inputs) + 1)) - 20, 40, 40)
                                if in_port_rect.collidepoint(m_pos):
                                    g.input_conns[i] = selected_obj
                    for obj in sb_nodes + sb_gates: obj.dragging = False
                    temp_wire_start = None
                    selected_obj = None

        # Dragging Logic
        if mode == "SANDBOX" and selected_obj and hasattr(selected_obj, 'dragging') and selected_obj.dragging:
            selected_obj.rect.center = m_pos

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()