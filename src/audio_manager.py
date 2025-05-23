import pygame
import os
from config import AUDIO_DIR

class AudioManager:
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.init()
        
        # Update paths to include the 'theme' subdirectory
        # Music tracks for different game modes
        self.music_tracks = {
            "menu": os.path.join(AUDIO_DIR, "theme", "menu_theme.mp3"),
            "normal": os.path.join(AUDIO_DIR, "theme", "main_gamemode_theme.mp3"),
            "lava": os.path.join(AUDIO_DIR, "theme", "lava_mode_theme.mp3"),
            "ice": os.path.join(AUDIO_DIR, "theme", "ice_theme.mp3")
        }
        
        # Sound effects dictionary
        self.sound_effects = {
            "coin": os.path.join(AUDIO_DIR, "sound_effect", "coin-recieved-230517.mp3")
        }
        
        # Load sound effects
        self.loaded_sounds = {}
        for sound_name, sound_path in self.sound_effects.items():
            try:
                self.loaded_sounds[sound_name] = pygame.mixer.Sound(sound_path)
            except pygame.error as e:
                print(f"Error loading sound effect {sound_name}: {e}")
        
        # Current playing track
        self.current_track = None
        
        # Volume settings
        self.music_volume = 0.5  # 50% volume by default
        self.sound_effect_volume = 0.7  # 70% volume for sound effects
        pygame.mixer.music.set_volume(self.music_volume)
        
        # Set volume for all loaded sound effects
        for sound in self.loaded_sounds.values():
            sound.set_volume(self.sound_effect_volume)
    
    def play_music(self, mode):
        """
        Play the music for the specified game mode.
        
        Args:
            mode (str): One of "menu", "normal", "lava", or "ice"
        """
        # Don't restart the same track
        if self.current_track == mode:
            return
            
        # Get the track path
        if mode in self.music_tracks:
            track_path = self.music_tracks[mode]
            
            # Check if the file exists
            if os.path.exists(track_path):
                try:
                    # Stop any currently playing music
                    pygame.mixer.music.stop()
                    
                    # Load and play the new track
                    pygame.mixer.music.load(track_path)
                    pygame.mixer.music.play(-1)  # Loop forever (-1)
                    self.current_track = mode
                    print(f"Now playing: {os.path.basename(track_path)}")
                except pygame.error as e:
                    print(f"Error playing music: {e}")
            else:
                print(f"Music file not found: {track_path}")
        else:
            print(f"Unknown game mode: {mode}")
    
    def play_sound(self, sound_name):
        """
        Play a sound effect once.
        
        Args:
            sound_name (str): Name of the sound effect to play
        """
        if sound_name in self.loaded_sounds:
            self.loaded_sounds[sound_name].play()
        else:
            print(f"Sound effect not found: {sound_name}")
    
    def stop_music(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
        self.current_track = None
    
    def set_volume(self, volume):
        """
        Set the music volume.
        
        Args:
            volume (float): Volume level between 0.0 and 1.0
        """
        # Ensure volume is within range
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
        # Also update sound effect volume if music is muted
        if volume == 0.0:
            for sound in self.loaded_sounds.values():
                sound.set_volume(0.0)
        else:
            for sound in self.loaded_sounds.values():
                sound.set_volume(self.sound_effect_volume)
    
    def pause_music(self):
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause the music."""
        pygame.mixer.music.unpause()

# Create a singleton instance
audio_manager = AudioManager() 