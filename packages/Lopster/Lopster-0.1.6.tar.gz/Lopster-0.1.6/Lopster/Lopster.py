import math
import inspect
import pygame
import pygame.font

class Event:
    _event = []
    def __init__(self, cond,event):
        self._event.append(self)
        self.cond = cond
        self.event = event

    def delete(self, sure):
        if sure:
            self._event.remove(self)
class Mouse:
    def __init__(self):
        pass
    def leftDown(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONDOWN:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 1:
                event(window, eve)
        ev = Event(evecond, even)
    def leftUp(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONUP:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 1:
                event(window, eve)
        ev = Event(evecond, even)
    def rightDown(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONDOWN:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 3:
                event(window, eve)
        ev = Event(evecond, even)
    def rightUp(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONUP:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 3:
                event(window, eve)
        ev = Event(evecond, even)
    def wheelUp(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONUP:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 2:
                event(window, eve)
        ev = Event(evecond, even)
    def wheelDown(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONDOWN:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 2:
                event(window, eve)
        ev = Event(evecond, even)
    def wheelForward(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONDOWN:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 4:
                event(window, eve)
        ev = Event(evecond, even)
    def wheelBack(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEBUTTONDOWN:
                return  True
            else:
                return False
        def even(window, eve):
            if eve.button == 5:
                event(window, eve)
        ev = Event(evecond, even)
    def move(self, event):
        def evecond(window, eve):
            if eve == pygame.MOUSEMOTION:
                return  True
            else:
                return False
        def even(window, eve):
            event(window, eve)
        ev = Event(evecond, even)
class Enemy:
    _object = []
    typ = "Enemy"

    def __init__(self, _x, _y, _h, _w, _update):
        self._object.append(self)
        self.x = _x
        self.y = _y
        self.h = _h
        self.w = _w
        self.update = _update

    def delete(self, sure):
        if sure:
            self._object.remove(self)

    def hide(self):
        self.typ = "NoN"

    def visible(self, typ):
        self.typ = typ

    def onClick(self, event):
        def is_clicked(window, eve):
            if self.x <= eve.pos[0] <= self.x + self.w and self.y <= eve.pos[1] <= self.y + self.h:
                event(window, eve)

        mouse = Mouse()
        mouse.leftDown(is_clicked)


class FakeEnemy:
    typ = "Enemy"
    x = 0
    y = 0
    h = 0
    w = 0
    def update(self): return print()

    def __init__(self, _x, _y, _h, _w, _update):
        self.x = _x
        self.y = _y
        self.h = _h
        self.w = _w
        self.update = _update

    def hide(self):
        self.typ = "NoN"

    def visible(self, typ):
        self.typ = typ


class Player(Enemy):
    typ = "EnemyPlayer"
    speed = 5

    def __init__(self, _x, _y, _h, _w, _update, speed):
        super().__init__(_x, _y, _h, _w, _update)
        self.speed = speed

    def addMove(self, up, down, left, right, obj):
        speed = self.speed
        keys = pygame.key.get_pressed()
        if keys[left]:
            obj.x -= speed
        if keys[right]:
            obj.x += speed
        if keys[up]:
            obj.y -= speed
        if keys[down]:
            obj.y += speed

    def addMoveWithBorder(self, up, down, left, right, obj, w, h):
        speed = self.speed
        keys = pygame.key.get_pressed()
        if keys[left] and obj.x >= self.w:
            obj.x -= speed
        if keys[right] and obj.x <= w - self.w:
            obj.x += speed
        if keys[up] and obj.y >= self.h:
            obj.y -= speed
        if keys[down] and obj.y <= h - self.h:
            obj.y += speed

    def moveRight(self):
        self.x += self.speed

    def moveLeft(self):
        self.x -= self.speed

    def moveUp(self):
        self.y -= self.speed

    def moveDown(self):
        self.y += self.speed

class Sprite(Enemy):
    def __init__(self, _x, _y, _h, _w, src, size, _update, speed):
        super().__init__(_x, _y, _h, _w, _update)
        self.speed = speed
        self.src = src
        self.size = size
        self.srcList = []
        self.count = 0

    def Animation(self, srcList):
        self.srcList = srcList
        self.count = 0

    def draw(self, window):
        window.blit(pygame.transform.scale(pygame.image.load(self.src), self.size), (self.x, self.y))

    def anim(self, window):
        if self.count >= len(self.srcList):
            self.count = 0
        else:
            pygame.time.delay(self.speed)
            window.blit(pygame.transform.scale(pygame.image.load(self.srcList[self.count]), self.size), (self.x, self.y))
            self.count += 1

    def cash(self):
        text = []

        text.append("Player\n")
        text.append("x = " + str(self.x) + "\n")
        text.append("y = " + str(self.y) + "\n")
        text.append("h = " + str(self.h) + "\n")
        text.append("w = " + str(self.w) + "\n")
        text.append("src = " + self.src + "\n")
        text.append("speed = " + str(self.speed) + "\n")
        text.append("size = " + str(self.size) + "\n")
        text.append("func update = " +
                    inspect.getsource(self.update).replace("\n", "/../+o+/../") + "\n")
        text.append("init @x @y @h @w @src @size @speed @update\n")
        text.append(";")

class Text(Enemy):
    def __init__(self, _x, _y, _h, _w, _update):
        super().__init__(_x, _y, _h, _w, _update)

    def draw(self, window, fontName, fontSize, text, color):
        font = pygame.font.Font(fontName, fontSize)
        _text = font.render(text, True, color)
        text_rect = _text.get_rect()
        text_rect.x = self.x
        text_rect.y = self.y
        window.blit(_text, text_rect)



class MathMap:
    h = 0
    w = 0

    def __init__(self, height, width):
        self._h = height
        self._w = width

    def Distance(self, obj, obj1):
        distance = math.sqrt((obj1.x - obj.x) ** 2 + (obj1.y - obj.y) ** 2)
        return distance

    def Side(self, x, y, x1, y1):
        if x1 > x:
            return "right"
        elif x1 < x:
            return "left"
        elif y1 > y:
            return "bottom"
        elif y1 < y:
            return "top"
        else:
            return "center"

    def isTouch(self, obj):
        for obj2 in obj._object:
            if obj != obj2:
                if obj.x < obj2.x + obj2.w and obj.x + obj.w > obj2.x and obj.y < obj2.y + obj2.h and obj.y + obj.h > obj2.y:
                    return True
        return False

    def getTouch(self, obj):
        for obj2 in obj._object:
            if obj != obj2:
                if obj.x < obj2.x + obj2.w and obj.x + obj.w > obj2.x and obj.y < obj2.y + obj2.h and obj.y + obj.h > obj2.y:
                    return obj2
        return None


class Map:
    def __init__(self, window, drawingMap):
        self.map = drawingMap
        self.window = window

    def draw(self, map):
        drawMap = self.map

        for card in map:
            if not type(card) == "tuple":
                drawMap[card](self.window, "NoN")
            else:
                for subCard in card:
                    drawMap[subCard](self.window, card)


class RunLopster:
    _fps = 16

    def __init__(self, window_size, title, icon, update, fps):
        self._window_size = window_size
        self._title = title
        self._update = update
        self._fps = fps
        self._icon = icon

    def run(self):
        window_size = self._window_size
        title = self._title
        update = self._update
        fps = self._fps
        icon = self._icon

        pygame.init()
        window = pygame.display.set_mode(window_size)

        pygame.display.set_caption(title)

        if(icon!=None):
            pygame.display.set_icon(pygame.image.load(icon))

        is_run = True

        while is_run:
            update(window)

            pygame.time.delay(1000 // fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_run = False

                for eve in Event._event:
                    if eve.cond(window, event.type):
                        eve.event(window, event)

            for obj in Enemy._object:
                if obj.typ != "NoN":
                    obj.update(window, obj)

            pygame.display.update()

        pygame.quit()