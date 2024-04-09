
def create_communicas(obj):
    # Section selection
    # Full examination
    obj.h1.setToolTip("Artifacts will be identified/corrected in the whole signal.")
    # Selected length
    obj.h2.setToolTip("Artifacts will be identified/corrected in the part of signal defined by 'Initial interval' and 'Last interval'.")
    # Set boundries
    obj.recount.setToolTip("Apply new boundaries based on the selection.")


    # Methods of identification
    # T1-T3
    obj.auto_art.setToolTip("...")
    # Tarvainen
    obj.poin_art.setToolTip("...")
    # Quotient
    obj.quot_art.setToolTip("....")
    # Manual
    obj.art_btn.setToolTip("Selected sample of RR Signal will be identified as an artifact.")
    # Delete single
    obj.del_btn.setToolTip("Selected sample of RR Signal will be removed from identified artifacts set.")
    # Delete all
    obj.clear_art.setToolTip("All artifacts selected with all algorithms will be removed from the set.")

    # Methods of correction
    # linear interpolation
    obj.m1.setToolTip("...")
    # cubic splain
    obj.m2.setToolTip("...")
    # deletion
    obj.m3.setToolTip("...")
    # moving average
    obj.m4.setToolTip("...")
    # pre mean
    obj.m5.setToolTip("...")