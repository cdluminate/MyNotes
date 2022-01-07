<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="DL&amp;CV" FOLDED="false" ID="ID_806386173" CREATED="1641242834029" MODIFIED="1641520995584" STYLE="oval">
<font NAME="Gentium" SIZE="18"/>
<hook NAME="MapStyle" zoom="1.464">
    <properties edgeColorConfiguration="#808080ff,#ff0000ff,#0000ffff,#00ff00ff,#ff00ffff,#00ffffff,#7c0000ff,#00007cff,#007c00ff,#7c007cff,#007c7cff,#7c7c00ff" fit_to_viewport="false"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node" STYLE="oval" UNIFORM_SHAPE="true" VGAP_QUANTITY="24.0 pt">
<font SIZE="24"/>
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right" STYLE="bubble">
<stylenode LOCALIZED_TEXT="default" ICON_SIZE="12.0 pt" COLOR="#000000">
<font NAME="Gentium" SIZE="10" BOLD="false" ITALIC="false"/>
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
<hook NAME="AutomaticEdgeColor" COUNTER="5" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Meta" LOCALIZED_STYLE_REF="styles.topic" POSITION="right" ID="ID_897570916" CREATED="1641520773367" MODIFIED="1641520995586">
<edge COLOR="#00ffff"/>
<font NAME="Gentium"/>
<node TEXT="what&apos;s this" ID="ID_34209772" CREATED="1641520840738" MODIFIED="1641520995587">
<font NAME="Gentium"/>
<node TEXT="Personal notes for regular paper reading." ID="ID_1963538377" CREATED="1641520844766" MODIFIED="1641520995588">
<font NAME="Gentium"/>
</node>
<node TEXT="starting from scratch again." ID="ID_531358300" CREATED="1641520859492" MODIFIED="1641520995589">
<font NAME="Gentium"/>
</node>
</node>
<node TEXT="Policy for this document" ID="ID_288232758" CREATED="1641520783594" MODIFIED="1641520995590">
<font NAME="Gentium"/>
<node TEXT="1. may include preprints, but only include them when I think they are relevant or helpful." ID="ID_608512408" CREATED="1641520800532" MODIFIED="1641520995590">
<font NAME="Gentium"/>
</node>
<node TEXT="2. gradually migrate the notes from the private mm&apos;s." ID="ID_1159004725" CREATED="1641520874706" MODIFIED="1641520995596">
<font NAME="Gentium"/>
</node>
</node>
</node>
<node TEXT="Face" LOCALIZED_STYLE_REF="styles.topic" POSITION="right" ID="ID_153988282" CREATED="1641242964517" MODIFIED="1641520995596">
<edge COLOR="#00ff00"/>
<font NAME="Gentium"/>
<node TEXT="Dataset" ID="ID_180339389" CREATED="1641503238612" MODIFIED="1641520995596">
<font NAME="Gentium"/>
<node TEXT="Casia webface" ID="ID_229244818" CREATED="1641503245897" MODIFIED="1641520995597">
<font NAME="Gentium"/>
<node TEXT="Learning Face Representation from Scratch" ID="ID_1940194677" CREATED="1641503251609" MODIFIED="1641520995568">
<icon BUILTIN="checked"/>
<font NAME="Gentium" ITALIC="true"/>
<node TEXT="no large scale dataset publically available, so propose semi-automatical way to collect face images" ID="ID_1189323012" CREATED="1641512559678" MODIFIED="1641520995597">
<font NAME="Gentium"/>
<node TEXT="CASIA-WebFace contains 1e4 subjects and 5e5 images." ID="ID_265616413" CREATED="1641512655754" MODIFIED="1641520995598">
<font NAME="Gentium"/>
</node>
</node>
<node TEXT="use a 11-layer CNN to learn discriminative feature. simply a multi-class classification baseline" ID="ID_1930071035" CREATED="1641512691353" MODIFIED="1641521098034"/>
<node TEXT="evaluate accuracy on LFW and YTF" ID="ID_421884912" CREATED="1641512706845" MODIFIED="1641520995599">
<font NAME="Gentium"/>
</node>
</node>
</node>
</node>
<node TEXT="Multi-Class Classification" ID="ID_1466249430" CREATED="1641243301668" MODIFIED="1641520995599">
<font NAME="Gentium"/>
<node TEXT="Center Loss" ID="ID_1925391381" CREATED="1641519035510" MODIFIED="1641520995599">
<font NAME="Gentium"/>
</node>
<node TEXT="SphereFace" ID="ID_312670993" CREATED="1641251036526" MODIFIED="1641520995600">
<font NAME="Gentium"/>
</node>
<node TEXT="CosFace" ID="ID_704538771" CREATED="1641251030859" MODIFIED="1641520995600">
<font NAME="Gentium"/>
</node>
<node TEXT="ArcFace: additive angular margin loss for deep face recognition" ID="ID_970043870" CREATED="1641242901225" MODIFIED="1641520995600">
<icon BUILTIN="checked"/>
<font NAME="Gentium"/>
<node TEXT="the two tracks of face recognition are multi-class classifier and embedding learning" ID="ID_611518023" CREATED="1641519055619" MODIFIED="1641520995601">
<font NAME="Gentium"/>
<node TEXT="problem for classification" ID="ID_1895607582" CREATED="1641519117849" MODIFIED="1641520995602">
<font NAME="Gentium"/>
<node TEXT="size of linear layer linearly increases with identity number" ID="ID_1714580233" CREATED="1641519128504" MODIFIED="1641520995602">
<font NAME="Gentium"/>
</node>
<node TEXT="learned features not discriminative enough in open-set setting" ID="ID_645674933" CREATED="1641519155123" MODIFIED="1641520995602">
<font NAME="Gentium"/>
</node>
</node>
<node TEXT="problem for embedding" ID="ID_1624119885" CREATED="1641519123374" MODIFIED="1641520995602">
<font NAME="Gentium"/>
<node TEXT="combinatorial explosion in triplets. increase number of iterations" ID="ID_167265516" CREATED="1641519176112" MODIFIED="1641520995602">
<font NAME="Gentium"/>
</node>
<node TEXT="semi-hard sample mining is difficult for effective training" ID="ID_1816861001" CREATED="1641519234769" MODIFIED="1641520995602">
<font NAME="Gentium"/>
</node>
</node>
</node>
<node TEXT="united formulation for sphereface, cosface and arcface" ID="ID_1920762886" CREATED="1641519314414" MODIFIED="1641520995602">
<font NAME="Gentium"/>
<node TEXT="\latex $$L_4=-\frac{1}{N}\sum_{i=1}^N \log \frac{&#xa;\exp(s\cos(m_1 \theta_{y_i} + m_2 )-m_3)&#xa;}{&#xa;\sum_j \exp(s\cos(m_1 \theta_{j} + m_2 )-m_3)&#xa;}$$" ID="ID_407559158" CREATED="1641519332807" MODIFIED="1641520995603">
<font NAME="Gentium"/>
</node>
<node TEXT="sphere face: multiplicative angular margin m_1" ID="ID_1612863665" CREATED="1641519483413" MODIFIED="1641520995603">
<font NAME="Gentium"/>
</node>
<node TEXT="arcface: additive angular margin m2" ID="ID_479788384" CREATED="1641519516270" MODIFIED="1641520995603">
<font NAME="Gentium"/>
</node>
<node TEXT="cosface: additive cosine margin m3" ID="ID_1469158039" CREATED="1641519549998" MODIFIED="1641520995603">
<font NAME="Gentium"/>
</node>
</node>
<node TEXT="https://github.com/deepinsight/insightface/tree/master/recognition/arcface_torch" ID="ID_1831504394" CREATED="1641519654585" MODIFIED="1641520995603">
<font NAME="Gentium"/>
</node>
</node>
</node>
<node TEXT="Embedding Learning" ID="ID_290828706" CREATED="1641243309778" MODIFIED="1641520995604">
<font NAME="Gentium"/>
<node TEXT="FaceNet" ID="ID_466452383" CREATED="1641242953447" MODIFIED="1641520995604">
<font NAME="Gentium"/>
</node>
</node>
</node>
<node TEXT="DML" LOCALIZED_STYLE_REF="styles.topic" POSITION="right" ID="ID_464750159" CREATED="1641242970936" MODIFIED="1641520995604">
<edge COLOR="#ff00ff"/>
<font NAME="Gentium"/>
<node TEXT="Survey" ID="ID_1192003468" CREATED="1641520461677" MODIFIED="1641520995604">
<font NAME="Gentium"/>
<node TEXT="revisiting ICML" ID="ID_367259996" CREATED="1641520468517" MODIFIED="1641520995604">
<font NAME="Gentium"/>
</node>
<node TEXT="reality ECCV" ID="ID_1508631828" CREATED="1641520470652" MODIFIED="1641520995604">
<font NAME="Gentium"/>
</node>
</node>
<node TEXT="Loss Functions" ID="ID_1262041414" CREATED="1641520453737" MODIFIED="1641520995604">
<font NAME="Gentium"/>
<node TEXT="Triplet" ID="ID_430004220" CREATED="1641242977534" MODIFIED="1641520995604">
<font NAME="Gentium"/>
</node>
<node TEXT="LiftStructure" ID="ID_362567920" CREATED="1641242980713" MODIFIED="1641520995605">
<font NAME="Gentium"/>
</node>
<node TEXT="Multi-Similarity" ID="ID_1503083507" CREATED="1641242994307" MODIFIED="1641520995605">
<font NAME="Gentium"/>
</node>
</node>
</node>
</node>
</map>
