<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.models import Wordform %>
<% from clld_morphology_plugin.util import get_further_lexemes %>
<%! active_menu_item = "lexemes" %>

<h3>${_('Lexeme')} <i>${ctx.name.upper()}</i></h3>

<dl>

% if ctx.description:
    <dt> ${_('Meaning')}: </dt>
    <dd> ${ctx.description} </dd>
% endif

% if ctx.base_lexemes:
        <dt> ${_('Derived from')}: </dt>
        <dd>
            % for lexlex in ctx.base_lexemes:
                ${h.link(request, lexlex.base_lexeme, label=lexlex.base_lexeme.name.upper())} ‘${lexlex.base_lexeme.description}’
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

% if ctx.derived_lexemes:
    <% further_lexemes = [] %>
    % for lexlex in ctx.derived_lexemes:
        <% further_lexemes.extend(get_further_lexemes(lexlex.derived_lexeme)) %>
    % endfor
    <dt> ${_('Derived lexemes')}: </dt>
    <dd>
        % for lex in further_lexemes:
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
${request.get_datatable('wordforms', Wordform, lexeme=ctx).render()}