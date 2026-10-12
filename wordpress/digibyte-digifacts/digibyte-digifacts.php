<?php
/**
 * Plugin Name:       DigiByte DigiFacts
 * Plugin URI:        https://github.com/DigiNode-Tools/digibyte-digifacts/tree/main/wordpress
 * Description:       Show a random DigiFact - a bite-size fact about DigiByte - that changes every minute. Available in multiple languages.
 * Version:           2.0.1
 * Requires at least: 5.0
 * Requires PHP:      7.4
 * Author:            Olly Stedall (DigiNode Tools)
 * Author URI:        https://diginode.tools
 * License:           GPL-2.0-or-later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       digibyte-digifacts
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const DIGIBYTE_DIGIFACTS_VERSION = '2.0.1';
// The DigiFacts website (https://github.com/DigiNode-Tools/digibyte-digifacts). Updated hourly.
const DIGIBYTE_DIGIFACTS_URL = 'https://digifacts.diginode.tools';
const DIGIBYTE_DIGIFACTS_REPO = 'https://github.com/DigiNode-Tools/digibyte-digifacts';
const DIGIBYTE_DIGIFACTS_SPONSOR = 'https://github.com/sponsors/DigiNode-Tools';

/**
 * Fetch a JSON file from the DigiFacts website. Each file is checked at most once an hour. If it can't be fetched,
 * the last good copy is used (and checked again in 10 minutes). Returns null if there has never been a good copy.
 *
 * @param string $path     e.g. 'en/html.json'
 * @param string $cache_id Short name for the cache, e.g. 'facts_en'
 */
function digibyte_digifacts_get_json( $path, $cache_id ) {
	$transient = 'digibyte_digifacts_' . $cache_id;
	$cached    = get_transient( $transient );
	if ( false !== $cached ) {
		return $cached ? $cached : null;
	}

	$data     = null;
	$response = wp_remote_get( DIGIBYTE_DIGIFACTS_URL . '/' . $path, array( 'timeout' => 5 ) );
	if ( ! is_wp_error( $response ) && 200 === wp_remote_retrieve_response_code( $response ) ) {
		$decoded = json_decode( wp_remote_retrieve_body( $response ), true );
		if ( is_array( $decoded ) && $decoded ) {
			$data = $decoded;
			update_option( $transient . '_last_good', $data, false );
		}
	}
	if ( ! $data ) {
		$data = get_option( $transient . '_last_good', null );
	}

	set_transient( $transient, $data ? $data : array(), $data ? HOUR_IN_SECONDS : 10 * MINUTE_IN_SECONDS );
	return $data;
}

/**
 * The available languages, as code => name (English first), from the DigiFacts website's info.json.
 */
function digibyte_digifacts_languages() {
	$info  = digibyte_digifacts_get_json( 'info.json', 'info' );
	$langs = array();
	if ( isset( $info['languages'] ) && is_array( $info['languages'] ) ) {
		foreach ( $info['languages'] as $code => $lang ) {
			if ( preg_match( '/^[a-z]{2}(-[a-z]{2,4})?$/', $code ) ) {
				$langs[ $code ] = isset( $lang['name'] ) ? (string) $lang['name'] : $code;
			}
		}
	}
	return $langs ? $langs : array( 'en' => 'English' );
}

/**
 * The DigiFacts for a language, ready to show: a list of array( 'title' => text, 'content' => safe HTML ).
 * Falls back to English if the language isn't available.
 */
function digibyte_digifacts_facts( $language ) {
	if ( ! preg_match( '/^[a-z]{2}(-[a-z]{2,4})?$/', $language ) ) {
		$language = 'en';
	}
	$raw = digibyte_digifacts_get_json( $language . '/html.json', 'facts_' . $language );
	if ( ! $raw && 'en' !== $language ) {
		$raw = digibyte_digifacts_get_json( 'en/html.json', 'facts_en' );
	}
	if ( ! is_array( $raw ) ) {
		return array();
	}

	// Only a link is allowed in a DigiFact (the DigiFacts website checks this too)
	$allowed = array(
		'a' => array(
			'href'   => true,
			'target' => true,
			'rel'    => true,
		),
	);
	$facts   = array();
	foreach ( $raw as $fact ) {
		if ( ! is_array( $fact ) || empty( $fact['title'] ) || empty( $fact['content'] ) ) {
			continue;
		}
		$content = wp_kses( (string) $fact['content'], $allowed );
		$content = str_replace( 'target="_blank"', 'target="_blank" rel="noopener"', $content );
		$facts[] = array(
			'title'   => wp_strip_all_tags( (string) $fact['title'] ),
			'content' => $content,
		);
	}
	return $facts;
}

/**
 * [digifacts] - shows a random DigiFact, which changes every minute.
 */
function digibyte_digifacts_shortcode() {
	$facts = digibyte_digifacts_facts( get_option( 'digibyte_digifacts_language', 'en' ) );
	if ( ! $facts ) {
		return ''; // Show nothing rather than an error
	}

	$fact = $facts[ array_rand( $facts ) ];
	$box  = 'text' !== get_option( 'digibyte_digifacts_display', 'box' );

	wp_enqueue_style( 'digibyte-digifacts' );
	wp_enqueue_script( 'digibyte-digifacts' );
	digibyte_digifacts_print_facts_once( $facts );

	return '<div class="digibyte-digifact' . ( $box ? ' with-box' : ' without-box' ) . '">'
		. '<h5 class="digifact-title">' . esc_html( $fact['title'] ) . '</h5>'
		. '<div class="digifact-content">' . $fact['content'] . '</div>'
		. '</div>';
}
add_shortcode( 'digifacts', 'digibyte_digifacts_shortcode' );

/**
 * Add the facts to the page once (for the script that changes the DigiFact every minute). Included in the page, so
 * it works with page caching and visitors' browsers don't need to contact any other site.
 */
function digibyte_digifacts_print_facts_once( $facts ) {
	static $done = false;
	if ( $done ) {
		return;
	}
	$done = true;
	wp_add_inline_script(
		'digibyte-digifacts',
		'window.digibyteDigiFacts = ' . wp_json_encode( $facts, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT ) . ';',
		'before'
	);
}

function digibyte_digifacts_register_assets() {
	wp_register_style( 'digibyte-digifacts', plugins_url( 'digifacts-styles.css', __FILE__ ), array(), DIGIBYTE_DIGIFACTS_VERSION );
	wp_register_script( 'digibyte-digifacts', plugins_url( 'js/digifact-refresh.js', __FILE__ ), array(), DIGIBYTE_DIGIFACTS_VERSION, true );
}
// Registered early ('init'), because block themes render the page content before 'wp_enqueue_scripts'
add_action( 'init', 'digibyte_digifacts_register_assets' );

/**
 * The DigiFacts block (shows the same as the shortcode).
 */
function digibyte_digifacts_register_block() {
	wp_register_script( 'digibyte-digifacts-block', plugins_url( 'js/block.js', __FILE__ ), array( 'wp-blocks', 'wp-element' ), DIGIBYTE_DIGIFACTS_VERSION, true );
	register_block_type(
		'digibyte/digifacts',
		array(
			'editor_script'   => 'digibyte-digifacts-block',
			'render_callback' => 'digibyte_digifacts_shortcode',
		)
	);
}
add_action( 'init', 'digibyte_digifacts_register_block' );

/*
 * Settings page: Settings > DigiFacts
 */

function digibyte_digifacts_admin_menu() {
	add_options_page( 'DigiByte DigiFacts', 'DigiFacts', 'manage_options', 'digibyte-digifacts', 'digibyte_digifacts_settings_page' );
}
add_action( 'admin_menu', 'digibyte_digifacts_admin_menu' );

function digibyte_digifacts_settings_init() {
	register_setting(
		'digibyte_digifacts_options',
		'digibyte_digifacts_language',
		array(
			'type'              => 'string',
			'default'           => 'en',
			'sanitize_callback' => 'digibyte_digifacts_sanitize_language',
		)
	);
	register_setting(
		'digibyte_digifacts_options',
		'digibyte_digifacts_display',
		array(
			'type'              => 'string',
			'default'           => 'box',
			'sanitize_callback' => 'digibyte_digifacts_sanitize_display',
		)
	);
	add_settings_section( 'digibyte_digifacts_section', '', '__return_false', 'digibyte-digifacts' );
	add_settings_field( 'digibyte_digifacts_language', 'Language', 'digibyte_digifacts_language_field', 'digibyte-digifacts', 'digibyte_digifacts_section' );
	add_settings_field( 'digibyte_digifacts_display', 'Display', 'digibyte_digifacts_display_field', 'digibyte-digifacts', 'digibyte_digifacts_section' );
}
add_action( 'admin_init', 'digibyte_digifacts_settings_init' );

function digibyte_digifacts_sanitize_language( $code ) {
	return array_key_exists( $code, digibyte_digifacts_languages() ) ? $code : 'en';
}

function digibyte_digifacts_sanitize_display( $display ) {
	return 'text' === $display ? 'text' : 'box';
}

function digibyte_digifacts_language_field() {
	$current = get_option( 'digibyte_digifacts_language', 'en' );
	echo '<select id="digibyte_digifacts_language" name="digibyte_digifacts_language">';
	foreach ( digibyte_digifacts_languages() as $code => $name ) {
		printf( '<option value="%s"%s>%s</option>', esc_attr( $code ), selected( $current, $code, false ), esc_html( $name ) );
	}
	echo '</select>';
	echo '<p class="description">A DigiFact that isn\'t translated yet is shown in English.</p>';
}

function digibyte_digifacts_display_field() {
	$display = get_option( 'digibyte_digifacts_display', 'box' );
	?>
	<label><input type="radio" name="digibyte_digifacts_display" value="box" <?php checked( $display, 'box' ); ?> /> Box</label><br />
	<label><input type="radio" name="digibyte_digifacts_display" value="text" <?php checked( $display, 'text' ); ?> /> Text only</label>
	<?php
}

function digibyte_digifacts_settings_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$facts = digibyte_digifacts_facts( get_option( 'digibyte_digifacts_language', 'en' ) );
	?>
	<div class="wrap">
		<h1>DigiByte DigiFacts</h1>
		<?php if ( ! $facts ) : ?>
			<div class="notice notice-warning"><p>The DigiFacts can't be loaded from <?php echo esc_html( DIGIBYTE_DIGIFACTS_URL ); ?> at the moment, so nothing is shown on your site. This is checked again every 10 minutes.</p></div>
		<?php endif; ?>
		<form action="options.php" method="post">
			<?php
			settings_fields( 'digibyte_digifacts_options' );
			do_settings_sections( 'digibyte-digifacts' );
			submit_button();
			?>
		</form>

		<h2>Usage</h2>
		<p>Add the <code>[digifacts]</code> shortcode, or the DigiByte DigiFacts block, where you want a DigiFact to appear. A random DigiFact is shown, and it changes every minute.</p>

		<h2>Styling</h2>
		<p>The DigiFacts use your theme's fonts and colours. To change how they look, add CSS in Appearance &gt; Customize &gt; Additional CSS. For example:</p>
		<pre>.digibyte-digifact .digifact-title { font-size: 1.2em; }
.digibyte-digifact.with-box { border-color: #0066cc; background: #f4f8ff; }</pre>

		<h2>Help improve the DigiFacts</h2>
		<p>Spotted a mistake, or a DigiFact that's out of date? Corrections, new DigiFacts and translations are all welcome - see <a href="<?php echo esc_url( DIGIBYTE_DIGIFACTS_REPO ); ?>" target="_blank" rel="noopener">how to contribute</a>.</p>
		<p>DigiFacts are maintained by <a href="https://diginode.tools" target="_blank" rel="noopener">DigiNode Tools</a>. If you find them useful, please consider <a href="<?php echo esc_url( DIGIBYTE_DIGIFACTS_SPONSOR ); ?>" target="_blank" rel="noopener">sponsoring DigiNode Tools</a>.</p>
	</div>
	<?php
}

/**
 * Tidy up after version 1.x (its browser cache and old options are no longer used).
 */
function digibyte_digifacts_upgrade() {
	if ( get_option( 'digibyte_digifacts_version' ) === DIGIBYTE_DIGIFACTS_VERSION ) {
		return;
	}
	delete_option( 'digibyte_digifacts_languages' );
	delete_transient( 'digibyte_digifacts_language_changed' );
	foreach ( array_keys( digibyte_digifacts_languages() ) as $code ) {
		delete_transient( 'digibyte_digifacts_' . $code ); // 1.x cache (old format)
	}
	update_option( 'digibyte_digifacts_version', DIGIBYTE_DIGIFACTS_VERSION );
}
add_action( 'admin_init', 'digibyte_digifacts_upgrade' );
