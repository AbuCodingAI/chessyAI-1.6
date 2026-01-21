/**
 * LESSON ENGINE
 * Interactive chess lessons for learning
 */

// Lesson Database - 5 beginner lessons
const LESSON_DATABASE = [
    {
        id: "lesson_001",
        title: "How the Pieces Move",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "Welcome to chess! Let's learn how each piece moves. We'll start with the pawn."
            },
            {
                type: "text",
                content: "The pawn moves forward one square. On its first move, it can move two squares forward."
            },
            {
                type: "diagram",
                fen: "8/8/8/8/8/8/4P3/8 w - - 0 1",
                caption: "The pawn can move to e3 or e4"
            }
        ]
    },
    {
        id: "lesson_002",
        title: "Basic Captures",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "In chess, you capture opponent pieces by moving your piece to their square."
            },
            {
                type: "text",
                content: "Pawns capture diagonally, one square forward. This is different from their normal move!"
            }
        ]
    },
    {
        id: "lesson_003",
        title: "Check and Checkmate",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "Check means the king is under attack. You must get out of check immediately!"
            },
            {
                type: "text",
                content: "Checkmate means the king is in check and cannot escape. Game over!"
            }
        ]
    },
    {
        id: "lesson_004",
        title: "Basic Tactics - The Fork",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "A fork is when one piece attacks two or more enemy pieces at once."
            },
            {
                type: "text",
                content: "Knights are excellent for forks because they can jump over pieces!"
            }
        ]
    },
    {
        id: "lesson_005",
        title: "Opening Principles",
        level: "beginner",
        sections: [
            {
                type: "text",
                content: "The opening is the first phase of the game. Follow these principles:"
            },
            {
                type: "text",
                content: "1. Control the center (e4, d4, e5, d5)\n2. Develop your pieces\n3. Castle early\n4. Don't move the same piece twice"
            }
        ]
    }
];

/**
 * Lesson Engine Class
 */
class LessonEngine {
    constructor() {
        this.currentLesson = null;
        this.sectionIndex = 0;
    }

    /**
     * Load a lesson by ID
     */
    loadLesson(lessonId) {
        this.currentLesson = LESSON_DATABASE.find(l => l.id === lessonId);
        this.sectionIndex = 0;
        return this.currentLesson;
    }

    /**
     * Get all lessons
     */
    getAllLessons() {
        return LESSON_DATABASE;
    }

    /**
     * Get current section
     */
    getCurrentSection() {
        if (!this.currentLesson) return null;
        return this.currentLesson.sections[this.sectionIndex];
    }

    /**
     * Move to next section
     */
    nextSection() {
        if (!this.currentLesson) return false;

        this.sectionIndex++;
        return this.sectionIndex < this.currentLesson.sections.length;
    }

    /**
     * Move to previous section
     */
    previousSection() {
        if (!this.currentLesson) return false;

        if (this.sectionIndex > 0) {
            this.sectionIndex--;
            return true;
        }
        return false;
    }

    /**
     * Check if lesson is complete
     */
    isComplete() {
        if (!this.currentLesson) return false;
        return this.sectionIndex >= this.currentLesson.sections.length - 1;
    }

    /**
     * Mark lesson as complete
     */
    markComplete() {
        if (!this.currentLesson) return;

        const progress = JSON.parse(localStorage.getItem('lessonProgress')) || {
            completed: [],
            current: null
        };

        if (!progress.completed.includes(this.currentLesson.id)) {
            progress.completed.push(this.currentLesson.id);
        }

        localStorage.setItem('lessonProgress', JSON.stringify(progress));
    }

    /**
     * Get lesson progress
     */
    getProgress() {
        return JSON.parse(localStorage.getItem('lessonProgress')) || {
            completed: [],
            current: null
        };
    }

    /**
     * Check if lesson is completed
     */
    isLessonCompleted(lessonId) {
        const progress = this.getProgress();
        return progress.completed.includes(lessonId);
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LessonEngine, LESSON_DATABASE };
}
