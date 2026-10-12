<?php
/**
 * Remove everything DigiByte DigiFacts stored, when the plugin is deleted.
 */

if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
	exit;
}

global $wpdb;

foreach ( array( 'digibyte_digifacts_language', 'digibyte_digifacts_display', 'digibyte_digifacts_version', 'digibyte_digifacts_languages' ) as $option ) {
	delete_option( $option );
}

// Cached DigiFacts and their last good copies (one per language), and 1.x leftovers
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '\_transient\_digibyte\_digifacts\_%' OR option_name LIKE '\_transient\_timeout\_digibyte\_digifacts\_%' OR option_name LIKE 'digibyte\_digifacts\_%\_last\_good'" );
