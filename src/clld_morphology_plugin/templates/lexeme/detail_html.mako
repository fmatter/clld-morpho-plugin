<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%! active_menu_item = "lexemes" %>

<h3>${_('Lexeme')} <i>${ctx.name}</i></h3>

% for f in ctx.forms:
${h.link(request, f.form)}
%endfor