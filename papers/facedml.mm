<map version="freeplane 1.7.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Face &amp; DML" FOLDED="false" ID="ID_806386173" CREATED="1641242834029" MODIFIED="1641242886360" STYLE="oval">
<font SIZE="18"/>
<hook NAME="MapStyle" zoom="1.61">
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
<hook NAME="AutomaticEdgeColor" COUNTER="4" RULE="ON_BRANCH_CREATION"/>
<node TEXT="Face" LOCALIZED_STYLE_REF="styles.topic" POSITION="right" ID="ID_153988282" CREATED="1641242964517" MODIFIED="1641243078822">
<edge COLOR="#00ff00"/>
<node TEXT="Dataset" ID="ID_180339389" CREATED="1641503238612" MODIFIED="1641503240267">
<node TEXT="Casia webface" ID="ID_229244818" CREATED="1641503245897" MODIFIED="1641503250481">
<node TEXT="Learning Face Representation from Scratch" ID="ID_1940194677" CREATED="1641503251609" MODIFIED="1641512945845">
<icon BUILTIN="checked"/>
<font ITALIC="true"/>
<node TEXT="no large scale dataset publically available, so propose semi-automatical way to collect face images" ID="ID_1189323012" CREATED="1641512559678" MODIFIED="1641512648637"/>
<node TEXT="CASIA-WebFace contains 1e4 subjects and 5e5 images." ID="ID_265616413" CREATED="1641512655754" MODIFIED="1641512691077"/>
<node TEXT="use a 11-layer CNN to learn discriminative feature. simply a multi-class classification baseline" ID="ID_1930071035" CREATED="1641512691353" MODIFIED="1641512932004"/>
<node TEXT="evaluate accuracy on LFW and YTF" ID="ID_421884912" CREATED="1641512706845" MODIFIED="1641512714431"/>
</node>
</node>
</node>
<node TEXT="Multi-Class Classification" ID="ID_1466249430" CREATED="1641243301668" MODIFIED="1641243308757">
<node TEXT="SphereFace" ID="ID_312670993" CREATED="1641251036526" MODIFIED="1641251039003"/>
<node TEXT="CosFace" ID="ID_704538771" CREATED="1641251030859" MODIFIED="1641251034812"/>
<node TEXT="ArcFace" ID="ID_970043870" CREATED="1641242901225" MODIFIED="1641242969613"/>
</node>
<node TEXT="Embedding Learning" ID="ID_290828706" CREATED="1641243309778" MODIFIED="1641243314600">
<node TEXT="FaceNet" ID="ID_466452383" CREATED="1641242953447" MODIFIED="1641242968884"/>
</node>
</node>
<node TEXT="DML" LOCALIZED_STYLE_REF="styles.topic" POSITION="right" ID="ID_464750159" CREATED="1641242970936" MODIFIED="1641243085858">
<edge COLOR="#ff00ff"/>
<node TEXT="Triplet" ID="ID_430004220" CREATED="1641242977534" MODIFIED="1641242980178"/>
<node TEXT="LiftStructure" ID="ID_362567920" CREATED="1641242980713" MODIFIED="1641242993798"/>
<node TEXT="Multi-Similarity" ID="ID_1503083507" CREATED="1641242994307" MODIFIED="1641243003074"/>
</node>
</node>
</map>
