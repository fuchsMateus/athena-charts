# syntax_highlighting.py

from pygments import lex
from pygments.lexers.sql import SqlLexer
from pygments.token import Token

def apply_syntax_highlighting(query_text):
    code = query_text.get("1.0", "end")
    query_text.mark_set("range_start", "1.0")

    for tag in query_text.tag_names():
        query_text.tag_delete(tag)

    token_colors = {
        Token.Keyword: "#0000FF",    
        Token.Name: "#008000",        
        Token.Operator: "#FF4500",    
        Token.String: "#A52A2A",      
        Token.Number: "#FF00FF",      
        Token.Comment: "#AAAAAA"     
    }

    for token, content in lex(code, SqlLexer()):
        query_text.mark_set("range_end", f"range_start + {len(content)}c")
        color = token_colors.get(token, "#000000")  

        query_text.tag_add(str(token), "range_start", "range_end")
        query_text.tag_configure(str(token), foreground=color)
        query_text.mark_set("range_start", "range_end")
