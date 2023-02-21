import src.db as db
import src.translator.free_google_translate as free_google_translate
import src.translator.google_cloud_translate as google_cloud_translate

initialized_db_list = []

def translate(text, source_language_code, target_language_code, translator='free_google_translate'):
    # Check if db is initialized
    if translator not in initialized_db_list:
        try:
            db.trdb_ensure_table_exists(translator)
            initialized_db_list.append(translator)
        except Exception as e:
            print('Error initializing db: {}'.format(e))
            raise e

    # Check if translation is cached
    try:
        translation = db.trdb_find(
            translator,
            {
                'source': source_language_code,
                'target': target_language_code,
                'original': text
            }
        )
        if translation is not None:
            return translation['translation']
    except Exception as e:
        print('Error checking cache: {}'.format(e))
        raise e

    # Translate
    translated_text = None
    if translator == 'free_google_translate':
        translated_text =  free_google_translate.translate(text, source_language_code, target_language_code)
    elif translator == 'google_cloud_translate':
        translated_text = google_cloud_translate.translate(text, source_language_code, target_language_code)
    else:
        raise ValueError('Invalid translator: {}'.format(translator))
    
    # Cache translation
    try:
        db.trdb_insert_batch(translator, [(source_language_code, target_language_code, text, translated_text)])
    except Exception as e:
        print('Error caching translation: {}'.format(e))

    return translated_text
