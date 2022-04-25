<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "morphs" %>


<%doc><h2>${_('Morph')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morph')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Form:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td> Morpheme:</td>
            <td>${h.link(request, ctx.morpheme)}</td>
        </tr>
        <tr>
            <td> Meaning:</td>
            <td>
                ${ctx.morpheme.meaning}
            </td>
        </tr>
        % if cognates in dir(ctx):
        <tr>
            <td>Cognate set(s):</td>
            <td>
              <%
                cogsets = []
              %>
                    % for c in ctx.cognates:
                        % if c.cognateset not in cogsets:
                            <%
                                cogsets.append(c.cognateset)
                            %>
                        % endif
                    % endfor
                    ${h.text2html("*"+"+".join([h.link(request, c) for c in cogsets]))}
            </td>
            % for c in ctx.cognates:
                ${type(c.cognateset)}
            % endfor
        </tr>
        % endif
        % if contribution in dir(ctx):
        <tr>
            <td> Contribution:</td>
            <td>
                ${h.link(request, ctx.contribution)} by
% for contributor in ctx.contribution.primary_contributors:
${h.link(request, contributor)}
% endfor
            </td>
        </tr>
        % endif
    </tbody>
</table>

% if ctx.forms:
<h3>${_('Word forms')}</h3>
<ol>
% for s in ctx.forms:
<li>
    ${h.link(request, s.form)}
</li>
% endfor
</ol>    
% endif

% if sentence_assocs in dir(ctx):
<h3>${_('Sentences')}</h3>
<ol>
    % for a in ctx.sentence_assocs:
    
    <li>
        ${h.rendered_sentence(a.example)}
    </li>

    % endfor
</ol>
% endif
