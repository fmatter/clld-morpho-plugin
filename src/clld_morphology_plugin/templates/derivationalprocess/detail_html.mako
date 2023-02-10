<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<% from clld_morphology_plugin.util import render_wordforms %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>
% try:
    <%from clld_corpus_plugin.util import rendered_sentence %>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry
<%! active_menu_item = "processes" %>

<h3>${ctx.name} (${_('Derivational process')})</h3>

${ctx.description}

Applications:
<ul>
    % for deriv in ctx.derivations:
    <% parts = [] %>
    % for part in deriv.stemparts:
        <% parts.append(h.link(request, part.stempart.morph)) %>
    % endfor
    <li>${h.link(request, deriv.source)}→${h.link(request, deriv.target)} (${", ".join(parts) | n })</li>
    % endfor
</ul>   