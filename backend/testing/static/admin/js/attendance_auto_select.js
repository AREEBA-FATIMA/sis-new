// Auto-selection logic for attendance admin
(function($) {
    'use strict';
    
    $(document).ready(function() {
        // Function to auto-populate fields when student is selected
        function autoPopulateFromStudent() {
            var studentId = $('#id_student').val();
            if (studentId) {
                // Make AJAX call to get student details
                $.ajax({
                    url: '/api/attendance/students/' + studentId + '/',
                    method: 'GET',
                    success: function(data) {
                        // Auto-populate classroom (student's actual classroom)
                        if (data.classroom) {
                            $('#id_classroom').val(data.classroom.id);
                            
                            // Auto-populate class teacher from student's classroom
                            if (data.classroom.class_teacher) {
                                $('#id_class_teacher').val(data.classroom.class_teacher.id);
                            }
                        }
                        
                        // Auto-populate campus
                        if (data.campus) {
                            $('#id_campus').val(data.campus.id);
                        }
                        
                        // Show success message
                        showMessage('Student selected: ' + data.name + ' from ' + data.classroom.name, 'success');
                    },
                    error: function() {
                        console.log('Error fetching student details');
                        showMessage('Error loading student details', 'error');
                    }
                });
            } else {
                // Clear fields if no student selected
                $('#id_classroom').val('');
                $('#id_class_teacher').val('');
                $('#id_campus').val('');
            }
        }
        
        // Function to auto-populate teacher when classroom is selected
        function autoPopulateFromClassroom() {
            var classroomId = $('#id_classroom').val();
            var studentId = $('#id_student').val();
            
            if (classroomId) {
                // Make AJAX call to get classroom details
                $.ajax({
                    url: '/api/attendance/classrooms/' + classroomId + '/',
                    method: 'GET',
                    success: function(data) {
                        // Auto-populate class teacher
                        if (data.class_teacher) {
                            $('#id_class_teacher').val(data.class_teacher.id);
                        }
                        
                        // Check if selected classroom matches student's classroom
                        if (studentId) {
                            $.ajax({
                                url: '/api/attendance/students/' + studentId + '/',
                                method: 'GET',
                                success: function(studentData) {
                                    if (studentData.classroom && studentData.classroom.id != classroomId) {
                                        showMessage('Warning: Selected classroom does not match student\'s actual classroom!', 'warning');
                                    }
                                }
                            });
                        }
                        
                        showMessage('Classroom selected: ' + data.name, 'success');
                    },
                    error: function() {
                        console.log('Error fetching classroom details');
                        showMessage('Error loading classroom details', 'error');
                    }
                });
            } else {
                // Clear teacher field if no classroom selected
                $('#id_class_teacher').val('');
            }
        }
        
        // Function to show messages
        function showMessage(message, type) {
            var alertClass = type === 'success' ? 'alert-success' : 
                           type === 'warning' ? 'alert-warning' : 'alert-danger';
            
            // Remove existing messages
            $('.attendance-message').remove();
            
            // Add new message
            var messageHtml = '<div class="attendance-message alert ' + alertClass + '" style="margin: 10px 0; padding: 10px;">' + message + '</div>';
            $('.form-row:first').before(messageHtml);
            
            // Auto-hide success messages after 3 seconds
            if (type === 'success') {
                setTimeout(function() {
                    $('.attendance-message').fadeOut();
                }, 3000);
            }
        }
        
        // Bind events
        $('#id_student').on('change', autoPopulateFromStudent);
        $('#id_classroom').on('change', autoPopulateFromClassroom);
        
        // Auto-populate on page load if student is already selected
        if ($('#id_student').val()) {
            autoPopulateFromStudent();
        }
        
        // Auto-populate on page load if classroom is already selected
        if ($('#id_classroom').val()) {
            autoPopulateFromClassroom();
        }
    });
})(django.jQuery);