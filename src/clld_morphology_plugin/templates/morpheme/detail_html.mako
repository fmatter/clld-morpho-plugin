<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "morphemes" %>


<%doc><h2>${_('Morpheme')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morpheme')} <i>${ctx.name}</i></h3>

<table class="table table-nonfluid">
    <tbody>
<%doc>        <tr>
            <td>Label:</td>
            <td>${ctx.name}</td>
        </tr></%doc>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        <tr>
            <td>Allomorphs:</td>
            <td>
                % for i, morph in enumerate(ctx.allomorphs):
                    % if i < len(ctx.allomorphs)-1:
                        <% comma = "," %>
                    % else:
                        <% comma = "" %>
                    % endif
                <i>${h.link(request, morph)}</i>${comma}
                % endfor
            </td>
        </tr>
        <tr>
            <td> Meaning:</td>
            <td>
                ${ctx.meaning}
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
