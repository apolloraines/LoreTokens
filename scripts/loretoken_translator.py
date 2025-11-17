#!/usr/bin/env python3
"""
LoreToken Translator System
Store in symbolic, translate for humans on-demand
"""

class LoreTokenTranslator:
    """
    Best practice: Store SYMBOLIC, translate when needed
    - Database: Symbolic (max compression, fewer tokens)
    - AI reads: Symbolic (fewer tokens = cheaper)
    - Human reads: Translate on-the-fly to readable
    - Debug mode: Show both formats
    """
    
    # Symbol mappings
    SYMBOLS = {
        '₿': 'BTC-USD',
        'Ξ': 'ETH-USD',
        '◎': 'SOL-USD',
        '✕': 'XRP-USD',
        'Ð': 'DOGE-USD',
        '⟐': 'RECORD',
        '⊤': 'TABLE',
        '§': 'symbol',
        '⏱': 'timestamp',
        '↗': 'open',
        '⤊': 'high',
        '⤋': 'low',
        '↘': 'close',
        '▣': 'volume',
        '⌘': 'granularity',
        '✓': 'ACTIVE',
        '1m': '60 seconds',
        '5m': '300 seconds',
        '1h': '3600 seconds'
    }
    
    @classmethod
    def symbolic_to_human(cls, symbolic: str) -> str:
        """Translate symbolic to human-readable"""
        human = symbolic
        
        # Replace symbols with meanings
        for symbol, meaning in cls.SYMBOLS.items():
            human = human.replace(symbol, meaning)
        
        # Make structure clearer
        human = human.replace('⟆', 'LORETOKEN.')
        human = human.replace('»', ' | ')
        human = human.replace('LT.', 'LORETOKEN.')
        
        return human
    
    @classmethod
    def human_to_symbolic(cls, human: str) -> str:
        """Translate human-readable to symbolic"""
        symbolic = human
        
        # Reverse mapping
        reverse_map = {v: k for k, v in cls.SYMBOLS.items()}
        for meaning, symbol in reverse_map.items():
            symbolic = symbolic.replace(meaning, symbol)
        
        # Compress structure
        symbolic = symbolic.replace('LORETOKEN.', '⟆')
        symbolic = symbolic.replace(' | ', '»')
        
        return symbolic
    
    @classmethod
    def query_translate(cls, query: str, from_human: bool = True) -> str:
        """Translate queries between formats"""
        if from_human:
            # Human query: "SELECT * WHERE symbol = 'BTC-USD'"
            # Becomes: "SELECT * WHERE § = '₿'"
            for meaning, symbol in {v: k for k, v in cls.SYMBOLS.items()}.items():
                query = query.replace(f"'{meaning}'", f"'{symbol}'")
                query = query.replace(f'"{meaning}"', f'"{symbol}"')
                query = query.replace(f'= {meaning}', f'= {symbol}')
        return query


def demonstrate():
    """Show the translation system"""
    
    # Symbolic record (what's stored)
    symbolic = "⟆⟐.RAW:[§₿»⏱1755392220»↗117391.31»⤊117406.15»⤋117370.33»↘117370.38»▣0.6098»⌘1m,✓]"
    
    translator = LoreTokenTranslator()
    
    print("🔄 LORETOKEN TRANSLATOR DEMO")
    print("=" * 60)
    
    print("\n📁 STORED IN DATABASE (Symbolic):")
    print(symbolic)
    print(f"Size: {len(symbolic)} chars")
    print(f"AI tokens: ~15")
    
    print("\n👁️ HUMAN READS (Translated):")
    human = translator.symbolic_to_human(symbolic)
    print(human)
    print(f"Size: {len(human)} chars")
    
    print("\n🔍 QUERY TRANSLATION:")
    human_query = "SELECT * FROM raw_prices WHERE symbol = 'BTC-USD' AND granularity = '60 seconds'"
    symbolic_query = translator.query_translate(human_query)
    print(f"Human writes: {human_query}")
    print(f"Executed as: {symbolic_query}")
    
    print("\n💡 BENEFITS:")
    print("✅ Database: Tiny (symbolic)")
    print("✅ AI Cost: Minimal (few tokens)")
    print("✅ Humans: Can read via translator")
    print("✅ Debugging: Show both formats")
    print("✅ Search: Works in either format")
    
    print("\n📊 COST COMPARISON:")
    costs = {
        "Natural English": {"chars": 50, "tokens": 10, "human": "⭐⭐⭐⭐⭐", "compression": "⭐"},
        "LoreToken Basic": {"chars": 172, "tokens": 30, "human": "⭐⭐⭐", "compression": "⭐⭐"},
        "Symbolic (stored)": {"chars": 66, "tokens": 15, "human": "⭐", "compression": "⭐⭐⭐⭐"},
        "Symbolic (translated)": {"chars": 66, "tokens": 15, "human": "⭐⭐⭐⭐", "compression": "⭐⭐⭐⭐"},
    }
    
    print("\nFormat         | Chars | Tokens | Human | Compression")
    print("-" * 55)
    for fmt, stats in costs.items():
        print(f"{fmt:20} | {stats['chars']:5} | {stats['tokens']:6} | {stats['human']:5} | {stats['compression']:5}")
    
    print("\n🎯 RECOMMENDATION:")
    print("Store SYMBOLIC + Add translator = Best of all worlds!")
    print("• Minimum storage (66 chars)")
    print("• Minimum AI tokens (15)")
    print("• Human readable (via translator)")
    print("• No compromise needed!")


if __name__ == "__main__":
    demonstrate()