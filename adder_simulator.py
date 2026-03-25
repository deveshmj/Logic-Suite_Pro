import pygame
import sys

# --- CONFIGURATION & COLORS ---
WIDTH, HEIGHT = 1000, 600
FPS = 60

# Cyberpunk Palette
CLR_BG = (15, 23, 42)        # Slate 900
CLR_PANEL = (30, 41, 59)    # Slate 800
CLR_WIRE_OFF = (51, 65, 85) # Slate 700
CLR_SUM = (34, 211, 238)    # Cyan 400
CLR_CARRY = (74, 222, 128)  # Green 400
CLR_TEXT = (248, 250, 252)  # White/Slate 50
CLR_ACCENT = (244, 114, 182) # Pink 400

class Gate:
    def __init__(self, x, y, type_name):
        self.rect = pygame.Rect(x, y, 120, 80)
        self.type = type_name # "XOR" or "AND"

    def draw(self, screen):
        # Draw Gate Body
        color = CLR_SUM if self.type == "XOR" else CLR_CARRY
        pygame.draw.rect(screen, color, self.rect, 2, border_radius=10)
        
        # Label inside gate
        font = pygame.font.SysFont("Arial", 24, bold=True)
        text = font.render(self.type, True, color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

class InputNode:
    def __init__(self, x, y, label):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.label = label
        self.state = 0 # 0 or 1

    def draw(self, screen):
        color = CLR_ACCENT if self.state == 1 else CLR_WIRE_OFF
        pygame.draw.rect(screen, color, self.rect, 0, border_radius=15)
        pygame.draw.rect(screen, CLR_TEXT, self.rect, 2, border_radius=15)
        
        font = pygame.font.SysFont("Arial", 32, bold=True)
        text = font.render(str(self.state), True, CLR_TEXT)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        
        # Label A or B
        lbl_font = pygame.font.SysFont("Arial", 18)
        lbl_text = lbl_font.render(f"Input {self.label}", True, CLR_TEXT)
        screen.blit(lbl_text, (self.rect.x, self.rect.y - 25))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Visual Half-Adder Simulator | Methodology PS#08")
    clock = pygame.time.Clock()
    
    # 1. Initialize Components
    node_a = InputNode(150, 200, "A")
    node_b = InputNode(150, 350, "B")
    
    xor_gate = Gate(500, 150, "XOR")
    and_gate = Gate(500, 380, "AND")

    while True:
        # --- EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if node_a.rect.collidepoint(event.pos):
                    node_a.state = 1 - node_a.state
                if node_b.rect.collidepoint(event.pos):
                    node_b.state = 1 - node_b.state

        # --- LOGIC CALCULATION ---
        # Half Adder Logic: Sum = A XOR B, Carry = A AND B
        sum_out = node_a.state ^ node_b.state
        carry_out = node_a.state & node_b.state

        # --- RENDERING ---
        screen.fill(CLR_BG)
        
        # Header text
        header_font = pygame.font.SysFont("Arial", 28, bold=True)
        header = header_font.render("Digital Half-Adder Simulator", True, CLR_TEXT)
        screen.blit(header, (WIDTH//2 - header.get_width()//2, 30))
        
        sub_header = pygame.font.SysFont("Arial", 16).render("Methodology: PS#08 | Developed by Team Devesh, Amitabh, Mrithula", True, CLR_WIRE_OFF)
        screen.blit(sub_header, (WIDTH//2 - sub_header.get_width()//2, 70))

        # Draw Wires (Background/Inactive)
        # From A to XOR
        pygame.draw.line(screen, CLR_ACCENT if node_a.state else CLR_WIRE_OFF, (210, 230), (500, 180), 4)
        # From B to XOR
        pygame.draw.line(screen, CLR_ACCENT if node_b.state else CLR_WIRE_OFF, (210, 380), (500, 200), 4)
        
        # From A to AND
        pygame.draw.line(screen, CLR_ACCENT if node_a.state else CLR_WIRE_OFF, (210, 230), (500, 410), 4)
        # From B to AND
        pygame.draw.line(screen, CLR_ACCENT if node_b.state else CLR_WIRE_OFF, (210, 380), (500, 430), 4)

        # Draw Components
        node_a.draw(screen)
        node_b.draw(screen)
        xor_gate.draw(screen)
        and_gate.draw(screen)
        
        # Output Wires
        pygame.draw.line(screen, CLR_SUM if sum_out else CLR_WIRE_OFF, (620, 190), (800, 190), 6)
        pygame.draw.line(screen, CLR_CARRY if carry_out else CLR_WIRE_OFF, (620, 420), (800, 420), 6)
        
        # Output Results
        res_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        sum_txt = res_font.render(str(sum_out), True, CLR_SUM if sum_out else CLR_WIRE_OFF)
        screen.blit(sum_txt, (820, 170))
        screen.blit(pygame.font.SysFont("Arial", 18).render("SUM", True, CLR_SUM), (815, 215))
        
        carry_txt = res_font.render(str(carry_out), True, CLR_CARRY if carry_out else CLR_WIRE_OFF)
        screen.blit(carry_txt, (820, 400))
        screen.blit(pygame.font.SysFont("Arial", 18).render("CARRY", True, CLR_CARRY), (815, 445))

        # Instructions
        instr = pygame.font.SysFont("Arial", 14).render("Click Input Nodes A or B to toggle logic state", True, CLR_WIRE_OFF)
        screen.blit(instr, (20, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()