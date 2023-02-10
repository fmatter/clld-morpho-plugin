<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "glosses" %>

<h3>${_('Gloss')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td> Morphs:</td>
            <td>
                <ul>
                   % for morph in ctx.morphs:
                       <li> ${h.link(request, morph)} </li>
                   % endfor
                </ul>
            </td>
        </tr>
        % if ctx.values:
            <tr>
                <td> Inflectional values:</td>
                <td>
                    <ul>
                       % for value in ctx.values:
                           <li>${h.link(request, value, label=value.name)} (${h.link(request, value.category)})</li>
                       % endfor
                    </ul>
                </td>
            </tr>
        % endif
        <tr>
            <td> Meanings:</td>
            <td>
                <ul>
                   ## % for meaning in ctx.morpheme.meanings:
                   ##     <li> ‘${h.link(request, meaning.meaning)}’ </li>
                   ## % endfor
                </ul>
            </td>
        </tr>
        <tr>
            <td> Forms:</td>
            <td>
                <ul>
                   % for fslice in ctx.formglosses:
                   <li>${h.link(request, fslice.formpart.form)}</li>
                   % endfor
                </ul>
            </td>
        </tr>
    </tbody>
</table>


<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>