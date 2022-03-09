CKEDITOR.editorConfig = function( config ) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';
    // ALLOW <span></span> and <span>&nbsp;</span>
    config.protectedSource.push(/<span[^>]*>(&nbsp;)?<\/span>/g);
};
CKEDITOR.dtd.$removeEmpty['span'] = false;
