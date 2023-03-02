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
        % if ctx.morphs:
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
        % endif
        % if ctx.stemglosses:
            <tr>
                <td> Stems:</td>
                <td>
                    <ul>
                       % for stemgloss in ctx.stemglosses:
                           <li> ${h.link(request, stemgloss.stem)} </li>
                       % endfor
                    </ul>
                </td>
            </tr>
        % endif
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
        ## % if ctx.meanings:
        ##     <tr>
        ##         <td> Meanings:</td>
        ##         <td>
        ##             <ul>
        ##             </ul>
        ##         </td>
        ##     </tr>
        ## % endif
        % if ctx.formglosses:
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
        % endif
    </tbody>
</table>


<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>