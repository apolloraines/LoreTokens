#!/usr/bin/env python3
"""
LoreToken Format Converter - Generic version for SAIQL.DELTA.DEV
Converts between different LoreToken storage formats
"""
import re
from enum import Enum

class DBMode(Enum):
    """Database format modes"""
    LT = "lt"      # Standard LoreToken format
    LTS = "lts"    # Symbolic format
    LTU = "ltu"    # Underscore format
    AUTO = "auto"  # Auto-detect

class LoreTokenConverter:
    """Converts between different LoreToken formats"""
    
    # Generic symbolic mappings for LTS format
    # Can be extended by applications for domain-specific symbols
    SYMBOL_MAP = {
        'id': '🔑',
        'name': '📛',
        'type': '🏷',
        'value': '💎',
        'timestamp': '⏱',
        'status': '📊',
        'priority': '⚡',
        'category': '📁',
        'description': '📝',
        'user': '👤',
        'action': '⚙',
        'data': '💾',
        'config': '⚙️',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️',
        'success': '✅',
        'count': '#️⃣',
        'size': '📏',
        'path': '📂'
    }
    
    # Reverse mapping
    REVERSE_MAP = {v: k for k, v in SYMBOL_MAP.items()}
    
    @classmethod
    def detect_format(cls, line):
        """Detect the format of a line"""
        if any(symbol in line for symbol in cls.SYMBOL_MAP.values()):
            return DBMode.LTS
        elif line.startswith('__'):
            return DBMode.LTU
        elif '>>' in line:
            return DBMode.LT
        return None
    
    @classmethod
    def parse_line(cls, line, source_format=None):
        """Parse a line in any format to a dictionary"""
        if not line or not line.strip():
            return None
        
        # Auto-detect format if not specified
        if source_format is None or source_format == DBMode.AUTO:
            source_format = cls.detect_format(line)
        
        record = {}
        
        if source_format == DBMode.LTS:
            # Parse symbolic format
            parts = line.strip().split()
            for part in parts:
                if '>>' in part:
                    key, value = part.split('>>', 1)
                    # Convert symbol to standard key
                    standard_key = cls.REVERSE_MAP.get(key, key)
                    record[standard_key] = value
        
        elif source_format == DBMode.LTU:
            # Parse underscore format
            parts = line.strip().split()
            for part in parts:
                if '>>' in part:
                    key, value = part.split('>>', 1)
                    # Remove leading underscores
                    if key.startswith('__'):
                        key = key[2:]
                    record[key] = value
        
        else:  # LT format or unknown
            # Parse standard format
            parts = line.strip().split()
            for part in parts:
                if '>>' in part:
                    key, value = part.split('>>', 1)
                    record[key] = value
        
        return record if record else None
    
    @classmethod
    def convert_line(cls, line, target_format=DBMode.LT, source_format=None):
        """Convert a line from one format to another"""
        # Parse the line first
        record = cls.parse_line(line, source_format)
        if not record:
            return line
        
        # Convert to target format
        if target_format == DBMode.LTS:
            # Convert to symbolic format
            parts = []
            for key, value in record.items():
                symbol = cls.SYMBOL_MAP.get(key, key)
                parts.append(f"{symbol}>>{value}")
            return ' '.join(parts) + '\n'
        
        elif target_format == DBMode.LTU:
            # Convert to underscore format
            parts = []
            for key, value in record.items():
                parts.append(f"__{key}>>{value}")
            return ' '.join(parts) + '\n'
        
        else:  # LT format
            # Convert to standard format
            parts = []
            for key, value in record.items():
                parts.append(f"{key}>>{value}")
            return ' '.join(parts) + '\n'
    
    @classmethod
    def extend_symbols(cls, custom_symbols):
        """
        Extend the symbol map with custom domain-specific symbols
        
        Args:
            custom_symbols (dict): Additional symbol mappings
        
        Example:
            LoreTokenConverter.extend_symbols({
                'temperature': '🌡️',
                'pressure': '🔵',
                'humidity': '💧'
            })
        """
        cls.SYMBOL_MAP.update(custom_symbols)
        cls.REVERSE_MAP = {v: k for k, v in cls.SYMBOL_MAP.items()}

# Export
__all__ = ['LoreTokenConverter', 'DBMode']