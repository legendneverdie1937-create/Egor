import pygame, math, random

pygame.init()
win = pygame.display.set_mode((0, 0))
W, H = win.get_size()
clock = pygame.time.Clock()
TS = int(W / 16)

cafes = [pygame.Rect(c * TS, int(H * 0.14), int(TS * 2.5), int(TS * 0.75)) for c in range(1, 15, 4)]
desks = [pygame.Rect(c * TS, int(r * TS * 0.93), int(TS * 1.6), int(TS * 0.65)) for r in range(4, 7) for c in range(2, 14, 3)]
obst = cafes + desks

px, py, pr, p_speed, php = TS * 1.5, H - TS * 1.5, int(TS * 0.28), 5, 100
ex, py_e, er, ehp, estate, espeed, e_count = W - TS * 2, TS * 1.5, int(TS * 0.28), 100, "chill", 3.5, 0

friends, MAX_F = [], 3
tx, ty, tr, thp, tspeed, t_active = 0, 0, int(TS * 0.35), 120, 0.6, False
stones, puddles = [], []

sx, sy, s_act, has_s, s_type = 0, 0, False, False, "poison"
ix, iy, i_act, has_i = 0, 0, False, False
spx, spy, s_ang, s_fly, s_spd = 0, 0, 0, False, 12
p_exp, p_rad, p_mx, pex, pey = False, 0, 180, 0, 0

EV_F, EV_S, EV_T = pygame.USEREVENT + 1, pygame.USEREVENT + 2, pygame.USEREVENT + 3
pygame.time.set_timer(EV_F, 20000)
pygame.time.set_timer(EV_S, 10000)
pygame.time.set_timer(EV_T, 50000)
class Friend:
    def __init__(self, x, y):
        self.x = max(TS, min(W - TS, x + random.uniform(-90, 90)))
        self.y = max(TS, min(H - TS, y + random.uniform(-90, 90)))
        self.radius, self.hp, self.spd = int(TS * 0.24), 40, 1.2

class Stone:
    def __init__(self, sx, sy, tx, ty):
        self.x, self.y, self.radius, self.speed, self.angle = sx, sy, 6, 7, math.atan2(ty - sy, tx - sx)

class Puddle:
    def __init__(self, x, y):
        self.x, self.y, self.radius = x, y, 70

def sp_s():
    global sx, sy, s_act, s_type
    if cafes:
        t = random.choice(cafes)
        sx, sy, s_act, s_type = t.centerx, t.centery, True, "pea" if random.randint(1, 100) <= 30 else "poison"

def sp_i():
    global ix, iy, i_act
    if desks:
        t = random.choice(desks)
        ix, iy, i_act = t.centerx, t.centery, True

def col(x, y, r):
    cr = pygame.Rect(x - r, y - r, r * 2, r * 2)
    return any(cr.colliderect(o) for o in obst)

sp_s(); sp_i(); friends.append(Friend(ex, py_e)); flash, t_cool, run = 0, 0, True
while run:
    win.fill((220, 155, 95))
    pygame.draw.line(win, (160, 100, 50), (0, H // 2 - 20), (W, H // 2 - 20), 4)
    for t in cafes:
        pygame.draw.rect(win, (70, 120, 180), t, 0, 6); pygame.draw.rect(win, (40, 80, 130), t, 3, 6)
    for d in desks:
        pygame.draw.rect(win, (110, 55, 25), d, 0, 4); pygame.draw.rect(win, (70, 30, 10), d, 2, 4)
    for p in puddles:
        pygame.draw.circle(win, (40, 20, 90), (int(p.x), int(p.y)), p.radius)
        pygame.draw.circle(win, (25, 10, 60), (int(p.x), int(p.y)), int(p.radius * 0.8))
    if s_act and not has_s:
        pygame.draw.circle(win, (255, 255, 255), (int(sx), int(sy)), int(TS * 0.25))
        pygame.draw.circle(win, (230, 200, 30) if s_type == "pea" else (40, 210, 40), (int(sx), int(sy)), int(TS * 0.14))
    if i_act and not has_i:
        pygame.draw.circle(win, (70, 40, 150), (int(ix), int(iy)), int(TS * 0.18))
        pygame.draw.circle(win, (255, 255, 255), (int(ix), int(iy)), int(TS * 0.08))

    m_pos = pygame.mouse.get_pos(); m_clk = pygame.mouse.get_pressed()
    JX, JY, JR, HR = 150, H - 120, 60, pygame.Rect(W - 180, H - 150, 120, 90)

    if m_clk and math.hypot(m_pos[0] - JX, m_pos[1] - JY) < JR + 20:
        ang = math.atan2(m_pos[1] - JY, m_pos[0] - JX)
        npx, npy = px + math.cos(ang) * p_speed, py + math.sin(ang) * p_speed
        if pr <= npx <= W - pr and pr <= npy <= H - pr and not col(npx, npy, pr): px, py = npx, npy

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: run = False
        if ev.type == EV_F and len(friends) < MAX_F: friends.append(Friend(ex, py_e))
        if ev.type == EV_S: [stones.append(Stone(f.x, f.y, px, py)) for f in friends]
        if ev.type == EV_T and not t_active: tx, ty, thp, t_active = W // 2, 50, 120, True
        if ev.type == pygame.MOUSEBUTTONDOWN and HR.collidepoint(ev.pos):
            if has_i: puddles.append(Puddle(px, py)); has_i = False; sp_i()
            elif has_s:
                if s_type == "poison" and not s_fly: spx, spy, s_ang, s_fly, has_s = px, py, math.atan2(py_e - py, ex - px), True, False
                elif s_type == "pea" and not p_exp: pex, pey, p_rad, p_exp, has_s, php = px, py, 10, True, False, min(100, php + 30)
            elif s_act and not has_s and math.hypot(sx - px, sy - py) < TS * 1.5: has_s, s_act = True, False
            elif i_act and not has_i and not has_s and math.hypot(ix - px, iy - py) < TS * 1.5: has_i, i_act = True, False
            else:
                if math.hypot(ex - px, py_e - py) < TS * 1.4: ehp -= 20; flash, estate = 5, "run"
                if t_active and math.hypot(tx - px, ty - py) < TS * 1.5:
                    thp -= 20; flash = 5
                    if thp <= 0: t_active = False
                for f in friends[:]:
                    if math.hypot(f.x - px, f.y - py) < TS * 1.4:
                        f.hp -= 20; flash = 5
                        if f.hp <= 0: friends.remove(f)

    if s_fly:
        spx += math.cos(s_ang) * s_spd; spy += math.sin(s_ang) * s_spd
        pygame.draw.circle(win, (255, 255, 255), (int(spx), int(spy)), int(TS * 0.2))
        pygame.draw.circle(win, (40, 210, 40), (int(spx), int(spy)), int(TS * 0.11))
        if math.hypot(ex - spx, py_e - spy) < er * 1.5: ehp -= 45; s_fly, estate, flash = False, "run", 8; sp_s()
        if t_active and math.hypot(tx - spx, ty - spy) < tr * 1.5:
            thp -= 45; s_fly, flash = False, 8
            if thp <= 0: t_active = False
            sp_s()
        for f in friends[:]:
            if math.hypot(f.x - spx, f.y - spy) < f.radius * 1.5:
                f.hp -= 45; s_fly, flash = False, 8
                if f.hp <= 0: friends.remove(f)
                sp_s()
        if not (0 <= spx <= W and 0 <= spy <= H): s_fly = False; sp_s()

    if p_exp:
        p_rad += 10; pygame.draw.circle(win, (180, 220, 30), (int(pex), int(pey)), p_rad, 4)
        if math.hypot(ex - pex, py_e - pey) < p_rad and estate != "run": ehp -= 50; estate = "run"
        if t_active and math.hypot(tx - pex, ty - pey) < p_rad:
            thp -= 50
            if thp <= 0: t_active = False
        for f in friends[:]:
            if math.hypot(f.x - pex, f.y - pey) < p_rad:
                f.hp -= 50
                if f.hp <= 0: friends.remove(f)
        if p_rad >= p_mx: p_exp = False; sp_s()

    for s in stones[:]:
        s.x += math.cos(s.angle) * s.speed; s.y += math.sin(s.angle) * s.speed
        pygame.draw.circle(win, (70, 70, 75), (int(s.x), int(s.y)), s.radius)
        if math.hypot(px - s.x, py - s.y) < pr + s.radius:
            php -= 15; stones.remove(s)
            if php <= 0: run = False
        elif not (0 <= s.x <= W and 0 <= s.y <= H): stones.remove(s)

    if ehp <= 0:
        e_count += 1; ehp, estate = 100, "chill"
        while True:
            rx, ry = random.uniform(TS, W - TS), random.uniform(TS, H - TS)
            if not col(rx, ry, er): ex, py_e = rx, ry; break

    ces = espeed / 2.5 if any(math.hypot(ex - p.x, py_e - p.y) < p.radius for p in puddles) else espeed
    if estate == "run":
        e_ang = math.atan2(py_e - py, ex - px)
        nex, ney = ex + math.cos(e_ang) * ces, py_e + math.sin(e_ang) * ces
        if er <= nex <= W - er and er <= ney <= H - er and not col(nex, ney, er): ex, py_e = nex, ney
        else: estate = "chill"

    for f in friends:
        f_ink = any(math.hypot(f.x - p.x, f.y - p.y) < p.radius for p in puddles)
        f.spd = 1.2 / 2.5 if f_ink else 1.2
        f_ang = math.atan2(py - f.y, px - f.x)
        f.x += math.cos(f_ang) * f.spd; f.y += math.sin(f_ang) * f.spd
        pygame.draw.circle(win, (40, 160, 40), (int(f.x), int(f.y)), f.radius)
        pygame.draw.circle(win, (245, 205, 165), (int(f.x), int(f.y - f.radius * 0.3)), int(f.radius * 0.7))
        pygame.draw.rect(win, (100, 0, 0), (int(f.x - 15), int(f.y - f.radius - 12), 30, 4))
        pygame.draw.rect(win, (200, 200, 0), (int(f.x - 15), int(f.y - f.radius - 12), int(30 * (f.hp / 40)), 4))

    if t_active:
        t_ink = any(math.hypot(tx - p.x, ty - p.y) < p.radius for p in puddles)
        cts = tspeed / 2.5 if t_ink else tspeed
        t_ang = math.atan2(py - ty, px - tx)
        tx += math.cos(t_ang) * cts; ty += math.sin(t_ang) * cts
        if math.hypot(tx - px, ty - py) < (tr + pr) and t_cool <= 0:
            php -= 20; t_cool = 60
            if php <= 0: run = False
        t_cool = max(0, t_cool - 1)
        pygame.draw.circle(win, (110, 110, 115), (int(tx), int(ty)), tr)
        pygame.draw.circle(win, (245, 205, 165), (int(tx), int(ty - tr * 0.3)), int(tr * 0.7))
        pygame.draw.circle(win, (50, 100, 200), (int(tx - 6), int(ty - tr * 0.3)), 4, 1)
        pygame.draw.circle(win, (50, 100, 200), (int(tx + 6), int(ty - tr * 0.3)), 4, 1)
        pygame.draw.rect(win, (100, 0, 0), (int(tx - 25), int(ty - tr - 15), 50, 6))
        pygame.draw.rect(win, (255, 0, 255), (int(tx - 25), int(ty - tr - 15), int(50 * (thp / 120)), 6))

    if has_s:
        bc = (230, 200, 30) if s_type == "pea" else (40, 210, 40)
        pygame.draw.circle(win, bc, (int(px), int(py)), int(pr * 1.3), 3)
    elif has_i:
        pygame.draw.circle(win, (110, 50, 220), (int(px), int(py)), int(pr * 1.3), 3)

    pygame.draw.circle(win, (55, 105, 225), (int(px), int(py)), pr)
    pygame.draw.circle(win, (245, 205, 165), (int(px), int(py - pr * 0.3)), int(pr * 0.7))
    pygame.draw.circle(win, (225, 65, 65), (int(ex), int(py_e)), er)
    pygame.draw.circle(win, (245, 205, 165), (int(ex), int(py_e - er * 0.3)), int(er * 0.7))
    pygame.draw.rect(win, (100, 0, 0), (int(ex - 20), int(py_e - er - 15), 40, 6))
    pygame.draw.rect(win, (0, 255, 0), (int(ex - 20), int(py_e - er - 15), int(40 * (ehp / 100)), 6))

    if flash > 0: pygame.draw.circle(win, (255, 255, 255), (int(ex), int(py_e)), int(er * 1.6), 4); flash -= 1
    pygame.draw.circle(win, (145, 145, 145), (JX, JY), JR, 4); pygame.draw.circle(win, (55, 55, 55), (JX, JY), 14)

    btn_c = (230, 200, 30) if (has_s and s_type == "pea") else (40, 210, 40) if has_s else (110, 50, 220) if has_i else (45, 185, 45)
    pygame.draw.rect(win, btn_c, HR, 0, 12); pygame.draw.rect(win, (25, 105, 25), HR, 3, 12)

    font = pygame.font.Font(None, int(H * 0.05))
    win.blit(font.render(f"EGOR BEATEN: {e_count}", True, (255, 255, 255)), (30, 30))
    win.blit(font.render(f"YOUR HP: {max(0, int(php))}", True, (0, 255, 0) if php > 40 else (255, 0, 0)), (30, 75))
    txt = "BOOM!" if (has_s and s_type == "pea") else "SOUP!" if has_s else "INK!" if has_i else "HIT!"
    win.blit(font.render(txt, True, (255, 255, 255)), (HR.x + 25, HR.y + 30))

    pygame.display.flip(); clock.tick(60)
pygame.quit()
# build

