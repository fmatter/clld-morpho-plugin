<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%import clld_morphology_plugin.util as mutil%>
<%! active_menu_item = "units" %>


<%doc><h2>${_('Form')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Form')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        % if ctx.morphs:
        <tr>
            <td>Structure:</td>
            <td>
                    ${h.text2html("-".join([h.link(request, slice.morph, label=string) for string, slice in zip(ctx.segmented.split("-"), ctx.morphs)]))}
            </td>
        </tr>
        % endif
        <tr>
            <td> Meaning:</td>
            <td>
                ‘${ctx.meaning}’
            </td>
        </tr>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
    </tbody>
</table>

% if ctx.sentences:
<h3>${_('Sentences')}</h3>
<ol>
    % for a in ctx.sentences:
    
    <li>
        ${mutil.rendered_sentence(request, a.sentence)}
    </li>

    % endfor
</ol>
% endif
