module.exports = function (grunt) {
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
 
    grunt.initConfig({
        uglify: {
            options: {
                mangle: false
            },
            production: {
                files: {
                    'js/ugly.js': [
                        'js/controllers/**/*.js',
                        'js/directives/**/*.js',
                        'js/services/**/*.js',
                        'js/app.js'
                    ]
                }
            }
        },
        jshint: {
            base: {
                src: ['js/**/*.js', '!js/lib/*', '!js/ugly.js'],
                options: {
                    "-W099": true // allow mixed tabs and spaces
                }
            }
        },
        less: {
            development: {
                files: {
                    'css/style.css': 'css/style.less'
                }
            }
        },
        watch: {
            js: {
                files: ['js/**/*.js', '!js/ugly.js'],
                tasks: ['jshint', 'uglify']
            },
            css: {
                files: 'css/**/*.less',
                tasks: ['less']
            }
        },
    });
 
    grunt.registerTask('default', ['watch']);
};