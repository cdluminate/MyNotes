<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="T490 Stage" FOLDED="false" ID="ID_1517682621" CREATED="1646928857979" MODIFIED="1646928894623" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000" STYLE="fork">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.attributes">
<font SIZE="9"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.note" COLOR="#000000" BACKGROUND_COLOR="#ffffff" TEXT_ALIGN="LEFT"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000" STYLE="oval" SHAPE_HORIZONTAL_MARGIN="10.0 pt" SHAPE_VERTICAL_MARGIN="10.0 pt">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,5"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,6"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,7"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,8"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,9"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,10"/>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,11"/>
</stylenode>
</stylenode>
</map_styles>
</hook>
<hook NAME="AutomaticEdgeColor" COUNTER="3" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Backdoor Attack" POSITION="right" ID="ID_621969120" CREATED="1646928896139" MODIFIED="1646928902737">
<edge COLOR="#ff0000"/>
<node TEXT="Automobile" ID="ID_1807292891" CREATED="1646928903901" MODIFIED="1646928910994">
<node TEXT="Clean-Annotation Backdoor Attack against Lane Detection Systems in the Wild" ID="ID_444510611" CREATED="1646928911957" MODIFIED="1646928920668">
<icon BUILTIN="pencil"/>
<node TEXT="physical attack against lane deteciton" ID="ID_78672113" CREATED="1646928932402" MODIFIED="1646929021292"/>
<node TEXT="clean-annotation approach" ID="ID_638994819" CREATED="1646929021555" MODIFIED="1646929029315"/>
</node>
</node>
</node>
<node TEXT="Attack Detection" POSITION="right" ID="ID_1704034770" CREATED="1646929038562" MODIFIED="1646929042691">
<edge COLOR="#0000ff"/>
<node TEXT="multitask" ID="ID_141398745" CREATED="1646929096139" MODIFIED="1646932700896">
<node TEXT="Detecting Adversarial Perturbations in Multi-Task Perception" ID="ID_274457308" CREATED="1646929102998" MODIFIED="1646932772460">
<icon BUILTIN="pencil"/>
<icon BUILTIN="idea"/>
<node TEXT="(1) detection scheme" ID="ID_192159417" CREATED="1646929219206" MODIFIED="1646929223629">
<node TEXT="adversarial perturbations are detected by inconsistencies between extracted edges of the input image, the depth output, and the segmentation output." ID="ID_589474324" CREATED="1646929131734" MODIFIED="1646929153597"/>
<node TEXT="heterogenious ensemble" ID="ID_812924113" CREATED="1646929154693" MODIFIED="1646929165001">
<icon BUILTIN="info"/>
</node>
</node>
<node TEXT="(2) edge consistency" ID="ID_1581857855" CREATED="1646929227157" MODIFIED="1646932558765">
<node TEXT="loss between different modalities" ID="ID_1491267282" CREATED="1646932513095" MODIFIED="1646932519209"/>
</node>
<node TEXT="(3) multi-task adv attack" ID="ID_1353003322" CREATED="1646932559964" MODIFIED="1646932565527">
<node TEXT="fooling various tasks and the detection" ID="ID_1825015452" CREATED="1646932573883" MODIFIED="1646932587870"/>
</node>
</node>
</node>
</node>
<node TEXT="Adversarial Defense" POSITION="right" ID="ID_1792455725" CREATED="1646933220976" MODIFIED="1646933224968">
<edge COLOR="#00ff00"/>
<node TEXT="Reverse Cross Entropy" ID="ID_1881427141" CREATED="1646933225738" MODIFIED="1646933231428">
<node TEXT="Towards Robust Detection of Adversarial Examples" ID="ID_1202072415" CREATED="1646933239848" MODIFIED="1646933245962">
<icon BUILTIN="checked"/>
<node TEXT="jun zhu" ID="ID_1172403521" CREATED="1646933241345" MODIFIED="1646933242767"/>
<node TEXT="reverse cross entropy" ID="ID_1181285418" CREATED="1646933414379" MODIFIED="1646933418556">
<node TEXT="\latex $L_{CE}^\lambda (x,y)=L_{CE}(x,y)-\lambda R_y^T \log F(x)$" ID="ID_406004386" CREATED="1646934270616" MODIFIED="1646934299584"/>
</node>
<node TEXT="thresholding detect" ID="ID_1860751625" CREATED="1646933418741" MODIFIED="1646933426947"/>
<node TEXT="does not report adversarial example strength" ID="ID_1516966777" CREATED="1646934922811" MODIFIED="1646934935894">
<icon BUILTIN="button_cancel"/>
</node>
</node>
</node>
</node>
</node>
</map>
