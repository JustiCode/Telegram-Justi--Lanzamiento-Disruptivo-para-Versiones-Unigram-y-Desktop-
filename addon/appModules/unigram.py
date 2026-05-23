# -*- coding: utf-8 -*-

"""
Telegram Justi 1.0
Complemento NVDA para Telegram Unigram.

Autor:
Mauro Ocampo - JustiCode
"""

import time

import api
import tones
import ui
import wx
import appModuleHandler
import keyboardHandler
import logHandler
import scriptHandler

log = logHandler.log


class AppModule(appModuleHandler.AppModule):
    """AppModule principal para Telegram Unigram."""

    lastAudioGesture = 0

    # =========================================================
    # Utilidades internas
    # =========================================================

    def sendKey(self, keyName):
        """Envía una combinación de teclas."""

        try:
            gesture = keyboardHandler.KeyboardInputGesture.fromName(
                keyName
            )

            gesture.send()

            time.sleep(0.08)

        except Exception:
            log.exception(
                "Error enviando tecla: %s",
                keyName
            )

    def findObjectByName(self, obj, target):
        """
        Busca recursivamente un objeto
        por coincidencia parcial de nombre.
        """

        if not obj:
            return None

        try:
            name = obj.name or ""

            if target.lower() in name.lower():
                return obj

        except Exception:
            pass

        try:
            child = obj.firstChild

            while child:

                result = self.findObjectByName(
                    child,
                    target
                )

                if result:
                    return result

                child = child.next

        except Exception:
            pass

        return None

    def activateObject(self, obj):
        """
        Activa un objeto accesible.

        Primero intenta doAction().
        Si falla, enfoca y pulsa espacio.
        """

        if not obj:
            return False

        try:
            obj.doAction()
            return True

        except Exception:
            pass

        try:
            obj.setFocus()

            time.sleep(0.1)

            self.sendKey("space")

            return True

        except Exception:
            pass

        return False

    def activateNamedControl(
        self,
        targetName,
        successMessage=None,
        errorMessage=None,
        beepFrequency=1000
    ):
        """
        Busca y activa un control por nombre.
        """

        fg = api.getForegroundObject()

        try:
            control = self.findObjectByName(
                fg,
                targetName
            )

            if not control:

                if errorMessage:
                    ui.message(errorMessage)

                return False

            self.activateObject(control)

            tones.beep(beepFrequency, 100)

            if successMessage:
                ui.message(successMessage)

            return True

        except Exception:
            log.exception(
                "Error activando control: %s",
                targetName
            )

            if errorMessage:
                ui.message(errorMessage)

        return False

    # =========================================================
    # Eventos
    # =========================================================

    def event_gainFocus(self, obj, nextHandler):
        """
        Enfoca automáticamente
        la lista de chats al iniciar Unigram.
        """

        try:

            if (
                obj.windowClassName
                == "Windows.UI.Core.CoreWindow"
                and "Abrir menú de navegación"
                in obj.name
            ):

                def focusChats():

                    self.sendKey("tab")
                    time.sleep(0.1)

                    self.sendKey("tab")
                    time.sleep(0.1)

                    self.sendKey("tab")

                wx.CallLater(
                    1200,
                    focusChats
                )

        except Exception:
            log.exception(
                "Error enfocando lista de chats"
            )

        nextHandler()

    # =========================================================
    # Scripts
    # =========================================================

    def script_voiceMessage(self, gesture):
        """Graba o envía mensajes de voz."""

        currentTime = time.time()

        try:

            if (
                currentTime - self.lastAudioGesture
                < 0.5
            ):

                self.sendKey("control+enter")

                tones.beep(1200, 100)

                ui.message(
                    "Audio enviado"
                )

            else:

                gesture.send()

                tones.beep(700, 100)

                ui.message(
                    "Grabando"
                )

            self.lastAudioGesture = currentTime

        except Exception:
            log.exception(
                "Error gestionando audio"
            )

            ui.message(
                "No se pudo grabar el audio"
            )

    def script_playPauseAudio(self, gesture):
        """Reproduce o pausa mensajes de voz."""

        try:

            focus = api.getFocusObject()

            if focus and focus.name:

                text = focus.name.lower()

                if "mensaje de voz" in text:

                    try:
                        focus.doAction()

                        tones.beep(900, 50)

                        return

                    except Exception:
                        pass

                    playButton = self.findObjectByName(
                        focus,
                        "Reproducir"
                    )

                    if not playButton:

                        playButton = self.findObjectByName(
                            focus,
                            "Pausar"
                        )

                    if playButton:

                        self.activateObject(
                            playButton
                        )

                        tones.beep(900, 50)

                        return

        except Exception:
            log.exception(
                "Error reproduciendo audio"
            )

        gesture.send()

    def script_openProfile(self, gesture):
        """Abre el perfil del chat actual."""

        self.activateNamedControl(
            "últ. vez",
            successMessage="Perfil abierto",
            errorMessage="Perfil no encontrado",
            beepFrequency=900
        )

    def script_voiceCall(self, gesture):
        """Inicia una llamada de voz."""

        self.activateNamedControl(
            "Llamar",
            successMessage="Llamando",
            errorMessage="Botón llamar no encontrado"
        )

    def script_videoCall(self, gesture):
        """Inicia una videollamada."""

        self.activateNamedControl(
            "Videollamar",
            successMessage="Videollamada",
            errorMessage="Botón videollamada no encontrado",
            beepFrequency=1200
        )

    def script_endCall(self, gesture):
        """Finaliza una llamada."""

        self.activateNamedControl(
            "Finalizar",
            successMessage="Llamada finalizada",
            errorMessage="Botón finalizar no encontrado",
            beepFrequency=500
        )

    def script_attachMedia(self, gesture):
        """Abre el menú adjuntar multimedia."""

        self.activateNamedControl(
            "Adjuntar multimedia",
            successMessage="Adjuntar multimedia",
            errorMessage="Botón adjuntar multimedia no encontrado"
        )

    def script_newChat(self, gesture):
        """Abre la ventana nuevo chat."""

        self.activateNamedControl(
            "Nuevo chat",
            successMessage="Nuevo chat",
            errorMessage="Botón nuevo chat no encontrado"
        )

    def script_focusMessageEdit(self, gesture):
        """Enfoca el cuadro de mensaje."""

        fg = api.getForegroundObject()

        try:

            edit = self.findObjectByName(
                fg,
                "Mensaje"
            )

            if not edit:

                ui.message(
                    "Cuadro mensaje no encontrado"
                )

                return

            edit.setFocus()

            tones.beep(900, 100)

            ui.message(
                "Cuadro mensaje"
            )

        except Exception:
            log.exception(
                "Error enfocando cuadro mensaje"
            )

            ui.message(
                "No se pudo abrir el cuadro mensaje"
            )

    def script_openNavigationMenu(self, gesture):
        """Abre el menú de navegación."""

        self.activateNamedControl(
            "Abrir menú de navegación",
            successMessage="Menú de navegación",
            errorMessage="Menú no encontrado"
        )

    # =========================================================
    # Gestos
    # =========================================================

    __gestures = {
        "kb:control+r": "voiceMessage",
        "kb:space": "playPauseAudio",
        "kb:control+p": "openProfile",
        "kb:control+shift+l": "voiceCall",
        "kb:control+shift+v": "videoCall",
        "kb:control+shift+n": "endCall",
        "kb:control+shift+a": "attachMedia",
        "kb:control+n": "newChat",
        "kb:alt+e": "focusMessageEdit",
        "kb:control+a": "openNavigationMenu",
    }