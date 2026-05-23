# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files whenever possible.

from site_scons.site_tools.NVDATool.typings import (
	AddonInfo,
	BrailleTables,
	SymbolDictionaries,
)

from site_scons.site_tools.NVDATool.utils import _


# Add-on information
addon_info = AddonInfo(

	# Internal add-on identifier
	addon_name="TelegramJusti",

	# User-visible add-on name
	addon_summary=_("Telegram Justi"),

	# Add-on description
	addon_description=_(
		"""Complemento de accesibilidad para Telegram Desktop y Unigram.

Mejora la navegación mediante atajos de teclado optimizados para usuarios
de lectores de pantalla y personas con discapacidad visual.

Incluye funciones para:
- grabación y envío de mensajes de voz,
- reproducción y pausa de audios,
- llamadas y videollamadas,
- acceso rápido a chats y perfiles,
- adjuntar archivos multimedia,
- enfoque automático en la lista de chats,
- navegación accesible y productividad mejorada."""
	),

	# Version
	addon_version="1.0.0",

	# Changelog
	addon_changelog=_(
		"""Primera versión pública.

Características principales:
- Compatibilidad con Telegram Desktop y Unigram.
- Grabación y envío de mensajes de voz.
- Reproducción y pausa de audios.
- Llamadas de voz y videollamadas.
- Acceso rápido a perfiles y chats.
- Adjuntar multimedia mediante atajos.
- Enfoque automático en lista de chats."""
	),

	# Author
	addon_author="Mauro Ocampo JustiCode <drmauroocampo271@gmail.com>",

	# Documentation URL
	addon_url="https://github.com/JustiCode/Telegram-Justi",

	# Source code URL
	addon_sourceURL="https://github.com/JustiCode/Telegram-Justi",

	# Documentation filename
	addon_docFileName="readme.html",

	# NVDA compatibility
	addon_minimumNVDAVersion="2026.1",
addon_lastTestedNVDAVersion="2026.1.1",

	# Update channel
	addon_updateChannel=None,

	# License
	addon_license="GPL v2",
	addon_licenseURL="https://www.gnu.org/licenses/gpl-2.0.html",
)

# Python source files
pythonSources = [
	"addon/appModules/unigram.py",
]

# Translation sources
i18nSources = pythonSources + [
	"buildVars.py",
]

# Excluded files
excludedFiles = []

# Base language
baseLanguage = "es"

# Markdown extensions
markdownExtensions = [
	"markdown.extensions.tables",
]

# Braille tables
brailleTables: BrailleTables = {}

# Symbol dictionaries
symbolDictionaries: SymbolDictionaries = {}