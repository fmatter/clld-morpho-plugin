<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin.util import rendered_form %>
<% from clld_morphology_plugin.util import render_derived_stems %>
<% from clld_morphology_plugin import models %>
<link rel="stylesheet" href="${req.static_url('clld_morphology_plugin:static/clld-morphology.css')}"/>

% try:
    <%from clld_corpus_plugin.util import rendered_sentence%>
% except:
    <% rendered_sentence = h.rendered_sentence %>
% endtry 
<%! active_menu_item = "morphs" %>


<%doc><h2>${_('Morph')} ${ctx.name} (${h.link(request, ctx.language)})</h2>
</%doc>

<h3>${_('Morph')} <i>${ctx.name}</i> ‘${ctx.description}’</h3>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>Language:</td>
            <td>${h.link(request, ctx.language)}</td>
        </tr>
        % if ctx.glosses:
            <tr>
                <td>Glosses:</td>
                <td>
                    ${h.text2html(", ".join([".".join([h.link(request, gloss) for gloss in glosslist]) for glosslist in ctx.glosses]))}
                </td>
            </tr>
        %endif
        % if ctx.morpheme:
        <tr>
            <td> Morpheme:</td>
            <td>${h.link(request, ctx.morpheme)}</td>
        </tr>
        % endif
        % if ctx.inflectionalvalues:
        <tr>
            <td> Inflectional values:</td>
            <td>
            <ul>
              % for val in ctx.inflectionalvalues:
                 <li>${h.link(request, val, label=val.name)} (${h.link(request, val.category)})</li>
              % endfor
            </ul>
            </td>
        </tr>
        % endif
        % if ctx.morph_type:
        <tr>
            <td> Type:</td>
            <td>${ctx.morph_type}</td>
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

<% gloss_sentences = {} %>

% for fslice in ctx.formslices:
    % if hasattr(fslice.form, "sentence_assocs") and fslice.form.sentence_assocs:
        <% gloss = ".".join([str(x.gloss) for x in fslice.glosses]) %>
        <% gloss_sentences.setdefault(gloss, []) %>
        % for s in fslice.form.sentence_assocs:
            <% gloss_sentences[gloss].append(s.sentence) %>
        % endfor
    % endif
% endfor

% for sslice in ctx.stemslices:
    % for wf in sslice.stem.wordforms:
        % if hasattr(wf, "sentence_assocs") and wf.sentence_assocs:
            <% gloss = ".".join([str(x.gloss) for x in sslice.glosses]) %>
            <% gloss_sentences.setdefault(gloss, []) %>
            % for s in wf.sentence_assocs:
                <% gloss_sentences[gloss].append(s.sentence) %>
            % endfor
        % endif
    % endfor
% endfor



<div class="tabbable">
    <ul class="nav nav-tabs">
        % if gloss_sentences:
            <li class=${'active' if gloss_sentences else ''}><a href="#corpus" data-toggle="tab"> Corpus tokens </a></li>
        % endif
        % if ctx.formslices:
            <li class=${'' if gloss_sentences else 'active'}><a href="#forms" data-toggle="tab"> Wordforms </a></li>
        % endif
        % if ctx.stemslices:
            <li class=${'' if gloss_sentences or ctx.formslices else 'active'}><a href="#stems" data-toggle="tab"> Stems </a></li>
        % endif
    </ul>

    <div class="tab-content" style="overflow: visible;">
        <div id="forms" class="tab-pane ${'' if gloss_sentences else 'active'}">
            ${request.get_datatable('wordforms', models.Wordform, morph=ctx).render()}
        </div>

        <div id="stems" class="tab-pane ${'' if gloss_sentences or ctx.formslices else 'active'}">
            ${request.get_datatable('stems', models.Stem, morph=ctx).render()}
        </div>


        <div id="corpus" class="tab-pane ${'active' if gloss_sentences else ''}">
            % for gloss, sentences in gloss_sentences.items():
                <div id=${gloss}>
                    % if len(sentences) > 1:
                        <h5> As ‘${gloss}’:</h5>
                    % endif
                    ## <button type="button" class="btn btn-link" onclick="copyIDs('${gloss}-ids')">Copy sentence IDs</button>
                    <% stc_ids = [] %>
                    <ol class="example">
                        % for sentence in sentences:
                            % if sentence.id not in stc_ids:
                                ${rendered_sentence(request, sentence, sentence_link=True)}
                                <% stc_ids.append(sentence.id) %>
                            % endif
                        % endfor
                    </ol>
                </div>
                <script>
                    var highlight_div = document.getElementById("${gloss}");
                    var highlight_targets = highlight_div.querySelectorAll("*[name='${ctx.id}']")
                    console.log(highlight_targets)
                    for (index = 0; index < highlight_targets.length; index++) {
                        highlight_targets[index].classList.add("morpho-highlight");
                    }
                </script>
            % endfor
        </div>
    </div>  
</div>



<script src="${req.static_url('clld_morphology_plugin:static/clld-morphology.js')}"></script>