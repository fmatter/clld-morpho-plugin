<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.models import Wordform %>
<%! active_menu_item = "lexemes" %>

<h3>${_('Lexeme')} <i>${ctx.name.upper()}</i></h3>

<h4>${_('Forms')}:</h4>
${request.get_datatable('wordforms', Wordform, lexeme=ctx).render()}