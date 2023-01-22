<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "glosses" %>


<%doc><h2>${_('Gloss')} ${ctx.name}</h2>
</%doc>

<h3>${_('Gloss')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td> Forms:</td>
            <td>
                <ol>
                   % for fslice in ctx.formslices:
                       <li> ${h.link(request, fslice.form)} </li>
                   % endfor
                </ol>
            </td>
        </tr>
        <tr>
            <td> Morphs:</td>
            <td>
                <ol>
                   % for morph in ctx.morphs:
                       <li> ${h.link(request, morph)} </li>
                   % endfor
                </ol>
            </td>
        </tr>
        <tr>
            <td> Meanings:</td>
            <td>
                <ol>
                   ## % for meaning in ctx.morpheme.meanings:
                   ##     <li> ‘${h.link(request, meaning.meaning)}’ </li>
                   ## % endfor
                </ol>
            </td>
        </tr>
    </tbody>
</table>


<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>