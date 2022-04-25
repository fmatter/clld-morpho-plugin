<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_morphology_plugin.util as mutil%>
<%! active_menu_item = "sentences" %>

<%def name="sidebar()">
    % if ctx.value_assocs:
    <%util:well title="${_('Datapoints')}">
        <ul>
        % for va in ctx.value_assocs:
            % if va.value:
            <li>${h.link(request, va.value.valueset, label='%s: %s' % (va.value.valueset.parameter.name, va.value.domainelement.name if va.value.domainelement else va.value.name))}</li>
            % endif
        % endfor
        </ul>
    </%util:well>
    % endif
</%def>

<h2>${_('Sentence')} ${ctx.id}</h2>
<dl>
    <dt>${_('Language')}:</dt>
    <dd>${h.link(request, ctx.language)}</dd>
</dl>

${mutil.rendered_sentence(request, ctx)|n}