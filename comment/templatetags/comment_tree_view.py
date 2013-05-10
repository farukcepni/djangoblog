from django import template
register = template.Library()

@register.filter(name='comment_tree_view')
def comment_tree_view(comments):
    def inline_tree(data):
        html = '<ul>'
        for key, comment in data.items():
            html += '<li class="main-child" ' \
                    'onclick="this.appendChild(document.getElementById(\'comment-form\')); ' \
                    'document.getElementById(\'comment-parent\').value=' + str(comment.id) + '">' + \
                    comment.comment + \
                    "<small> -> Cevapla</small></li>"
            if len(comment.children) > 0:
                html += '<li class="has-child">' + inline_tree(comment.children) + "</li>"
        html += '</ul>'
        return html
    html_tree = inline_tree(comments)
    return html_tree
