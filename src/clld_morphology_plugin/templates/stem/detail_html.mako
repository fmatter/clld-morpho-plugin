<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.models import Wordform %>
<% from clld_morphology_plugin.util import get_further_stems %>
<%! active_menu_item = "stems" %>

<h3>${_('Stem')} <i>${ctx.name.upper()}</i></h3>

<dl>

% if ctx.description:
    <dt> ${_('Meaning')}: </dt>
    <dd> ${ctx.description} </dd>
% endif

% if ctx.base_stems:
        <dt> ${_('Derived from')}: </dt>
        <dd>
            % for lexlex in ctx.base_stems:
                ${h.link(request, lexlex.base_stem, label=lexlex.base_stem.name.upper())} ‘${lexlex.base_stem.description}’
            % endfor
        </dd>
% endif

% if ctx.derivational_morphemes:
    <dt> ${_('Derived with')}: </dt>
    <dd>
        % for lexmorph in ctx.derivational_morphemes:
            ${h.link(request, lexmorph.morpheme)}
        % endfor
    </dd>
% endif

% if ctx.derived_stems:
    <% further_stems = [] %>
    % for lexlex in ctx.derived_stems:
        <% further_stems.extend(get_further_stems(lexlex.derived_stem)) %>
    % endfor
    <dt> ${_('Derived stems')}: </dt>
    <dd>
        % for lex in further_stems:
            ${h.link(request, lex, label=lex.name.upper())}<br>
        % endfor
    </dd>
% endif

% if ctx.root_morpheme:
    <dt> ${_('Corresponding morpheme')}: </dt>
    <dd>
        ${h.link(request, ctx.root_morpheme)}
    </dd>
% endif

% if ctx.comment:
    <dt> ${_('Comment')}: </dt>
    <dd>
        ${parent.markdown(request, ctx.comment)|n}
    </dd>
% endif

</dl>


<h4>${_('Forms')}:</h4>
${request.get_datatable('wordforms', Wordform, stem=ctx).render()}