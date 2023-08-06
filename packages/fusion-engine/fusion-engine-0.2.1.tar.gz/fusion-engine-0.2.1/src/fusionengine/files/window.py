import fusionengine.files.systems as sysconfig
from fusionengine.files.imports import *

class _CustomRenderer:
    def __init__(self, window: SDL_CreateWindow) -> None:
        self.window = window
        self.event = SDL_Event()
        self.renderer = SDL_CreateRenderer(self.window, -1, sysconfig.RendererOptions().rendererflag)

class Window:
    def __init__(self) -> None:
        self.window = None
        self._running = False
        self._NOW = SDL_GetPerformanceCounter()
        self._LAST = 0
        self.DELTATIME = 0
        self._entity = []
    
    def new_window(self, title: str, width: int, height: int) -> _CustomRenderer:
        encoded_title = title.encode('utf-8')
        self.window_window = SDL_CreateWindow(encoded_title,
                                       SDL_WINDOWPOS_CENTERED,
                                       SDL_WINDOWPOS_CENTERED,
                                       width,
                                       height,
                                       SDL_WINDOW_SHOWN
                                       )
        self._running = True
        self.window = _CustomRenderer(self.window_window)
        return self.window
    
    def loop(self, your_loop):
        while self.running(self.window):
            your_loop()
    
    def running(self, window:_CustomRenderer) -> bool:
        self._refresh(window)
        return self._running
    
    def _refresh(self, window: _CustomRenderer) -> None:
        SDL_UpdateWindowSurface(window.window)
        SDL_RenderPresent(window.renderer)
        
        self._LAST = self._NOW
        self._NOW = SDL_GetPerformanceCounter()

        
        
        self.DELTATIME = (self._NOW - self._LAST)*1000 / SDL_GetPerformanceFrequency()
               
        if sdl2.SDL_PollEvent(window.event) != 0:
            if window.event.type == sdl2.SDL_QUIT:
                self._running = False

        
