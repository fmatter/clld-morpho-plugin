<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<% from clld_morphology_plugin.util import render_derived_from %>
<% from clld_morphology_plugin.util import render_derived_stems %>
<% from clld_morphology_plugin.models import Wordform %>
<%! active_menu_item = "stems" %>

<h3>${_('Stem')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        % if ctx.lexeme:
            <tr>
                <td> Lexeme: </td>
                <td> ${h.link(request, ctx.lexeme)}</td>
            </tr>        
        % endif
        % if ctx.glosses:
            <tr>
                <td> Gloss: </td>
                <td> ${h.text2html(", ".join([h.link(request, g) for g in ctx.glosses]))}</td>
            </tr>        
        % endif
        % if ctx.stemforms and not ctx.inflections:
            <tr>
                <td> Forms: </td>
                <td> ${h.text2html(", ".join([h.link(request, stemform.form) for stemform in ctx.stemforms]))}</td>
            </tr>
        % endif
        % if ctx.parts:
            <tr>
                <td> Structure: </td>
                <td>
                    ${rendered_form(request, ctx) | n}<br>
                    ${rendered_form(request, ctx, line="gloss") | n}<br>
                    ## ${rendered_form(request, ctx, level="stem") | n}<br>
                    ## ${rendered_form(request, ctx, level="stem", line="gloss") | n}
                </td>
            </tr>
        % endif
        % if ctx.derived_from:
            <tr>
                <td> ${_('Derivational lineage')}: </td>
                <td>
                    ${render_derived_from(request, ctx) | n}
                </td>
            </tr>
        % endif
        % if ctx.derivations:
            <tr>
                <td> ${_('Derived stems')}: </td>
                <td>
                    ${render_derived_stems(request, ctx)}
                </td>
            </tr>
        % endif
    </tbody>
</table>

<%def name="print_cell(entity)">
    % if isinstance(entity, str):
        ${entity}
    % else:
        ${h.link(request, entity)}
    % endif
</%def>

##% if ctx.inflections:
##<% paradigm = render_paradigm(ctx) %>
##Inflected forms:
##<table border="2">
##    % for col_idx, colname in enumerate(paradigm["colnames"]):
##        <tr>
##            % for x in range(len(paradigm["idxnames"])-1):
##                <td> </td>
##            % endfor
##            <th> ${h.link(request, colname)} </th>
##            % for column in paradigm["columns"]:
##                <th>
##                    % if not isinstance(column, tuple):
##                        ${print_cell(column)}
##                    % else:
##                        ${print_cell(column[col_idx])}
##                    % endif
##                </th>
##            % endfor
##        </tr>
##    % endfor
##    <tr>
##        % for idxname in paradigm["idxnames"]:
##            <th> 
##                ${print_cell(idxname)}
##            </th>
##        % endfor
##    </tr>
##        <tr>
##        % for idxnames, cells in zip(paradigm["index"], paradigm["cells"]):
##        <tr>
##            % for idxname in idxnames:
##            <th>
##                ${print_cell(idxname)}
##                </th>
##            % endfor
##            % for cell in cells:
##            <td>
##                % for form in cell:
##                    ${h.link(request, form)}
##                % endfor
##                </td>
##            % endfor
##        </tr>
##        % endfor
##    </tr>
## </table>
#### ${render_paradigm(ctx, html=True) | n}
##% endif

##<dl>
##% if ctx.base_stems:
##        <dt> ${_('Derived from')}: </dt>
##        <dd>
##            % for lexlex in ctx.base_stems:
##                ${h.link(request, lexlex.base_stem, label=lexlex.base_stem.name.upper())} ‘${lexlex.base_stem.description}’
##            % endfor
##        </dd>
##% endif
##
##% if ctx.derivational_morphemes:
##    <dt> ${_('Derived with')}: </dt>
##    <dd>
##        % for lexmorph in ctx.derivational_morphemes:
##            ${h.link(request, lexmorph.morpheme)}
##        % endfor
##    </dd>
##% endif
##

##
##% if ctx.root_morpheme:
##    <dt> ${_('Corresponding morpheme')}: </dt>
##    <dd>
##        ${h.link(request, ctx.root_morpheme)}
##    </dd>
##% endif
##
##% if ctx.comment:
##    <dt> ${_('Comment')}: </dt>
##    <dd>
##        ${parent.markdown(request, ctx.comment)|n}
##    </dd>
##% endif
##
##</dl>
##
##
<h4>${_('Wordforms')}:</h4>
${request.get_datatable('wordforms', Wordform, stem=ctx).render()}