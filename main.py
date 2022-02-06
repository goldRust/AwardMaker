from appJar import gui
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.pagesizes import portrait
from reportlab.lib.units import inch
from reportlab.lib.colors import white, red, darkred, black
from reportlab.platypus import Image

import classes


def create_awards(awards, folder, tournament, team_pic=None):

    award_count = 0
    pdf_file_name = tournament
    pdf = canvas.Canvas(folder + '\\' + pdf_file_name + '.pdf', pagesize=portrait(letter))
    ix_pos = 0
    iy_pos = 0
    xpos = 88
    first_ypos = 320
    last_ypos = 295
    event_ypos = 250
    place_ypos = 70

    gold = 'gold.png'
    silver = 'silver.png'
    bronze = 'bronze.png'

    for award in awards:
        # Assign the proper image for this award
        if int(award.place) == 1:
            image = gold
        elif int(award.place) == 2:
            image = silver
        else:
            image = bronze

        # Insert the image
        pdf.drawImage(image, ix_pos, iy_pos)

        # Set the font size for names
        name_font = 24

        # Check the length of the strings to see if the font size needs to change.
        if len(award.first) or len(award.last) > 9:
            name_font = 18

        event_font = 44 - 2.3*len(award.event)

        # Insert the text
        pdf.setFont('Courier', name_font, leading=None)
        pdf.drawCentredString(xpos + ix_pos, first_ypos + iy_pos, award.first)
        pdf.drawCentredString(xpos + ix_pos, last_ypos + iy_pos, award.last)
        pdf.setFont('Courier', event_font, leading=None)
        pdf.drawCentredString(xpos + ix_pos, event_ypos + iy_pos, award.event)
        pdf.setFont('Courier', 60, leading=None)
        pdf.drawCentredString(xpos + ix_pos, place_ypos + iy_pos, award.place)

        award_count += 1
        ix_pos += 200

        if award_count == 3:
            iy_pos += 400
            ix_pos = 0
        if award_count > 5:
            award_count = 0
            ix_pos = 0
            iy_pos = 0
            pdf.showPage()

    pdf.showPage()

    if team_pic is not None:
        team_picture(pdf, tournament, team_pic)

    pdf.save()


def team_picture(pdf, tournament, team_pic):

    team_name = 'Osage City High School'
    center_pic_x = 4.5 * inch
    tn_y = 4.25 * inch
    tourn_y = 1.25 * inch
    pdf.drawImage(team_pic, inch, inch, 7*inch, 4*inch)
    pdf.setFont('Courier', 32)
    pdf.drawCentredString(center_pic_x, tn_y, team_name)
    pdf.setFillColor(white)
    pdf.drawCentredString(center_pic_x, tourn_y, tournament)
    pdf.showPage()


def get_gui():
    app = gui('Forensics Awards Generator')
    awards = []
    team_pic = ''
    has_pic = False

    def select_folder():
        app.showSubWindow('save')

    def select_picture():
        app.showSubWindow('team_pic')

    def attach_pic():
        nonlocal team_pic, has_pic
        team_pic = app.getEntry('team_picture')
        has_pic = True
        app.hideAllSubWindows()

    def run_award_maker():
        folder = app.getEntry('Location:')
        name = app.getEntry('Tournament:')
        if has_pic:
            create_awards(awards, folder, name, team_pic)
        else:
            create_awards(awards, folder, name)
        more = app.yesNoBox('more', 'Awards created successfully! \n Would you like to make more?', parent='save')
        app.stop()
        if more:
            get_gui()

    def add_award():
        award = app.getTableEntries('award_table')
        app.addTableRow('award_table', award)
        first = award[0]
        last = award[1]
        event = award[2]
        place = award[3]
        new_award = classes.Award(first, last, event, place)

        awards.append(new_award)

    def remove(row):
        app.deleteTableRow('award_table', row)
        awards.pop(row)
        print(row)

    app.addLabelEntry('Tournament:')

    app.addTable('award_table', [['First Name', 'Last Name', 'Event', 'Place']], addRow=add_award, action=remove,
                 actionButton='Remove')
    app.addButtons(['Add Team Photo', 'Make Awards', 'Close'], [select_picture, select_folder, app.stop])

    app.startSubWindow('save', 'Save Awards')
    app.label('file_select_label', 'Where do you want to save the awards?')
    app.addDirectoryEntry('Location:')
    app.addButtons(['Cancel', 'Create Awards'], [app.hideAllSubWindows, run_award_maker])
    app.stopSubWindow()

    app.startSubWindow('team_pic', 'Team Photo')
    app.addLabel('tp_label', 'Attach Team Photo')
    app.addFileEntry('team_picture')
    app.addButtons(['Cancel Pic', 'Attach Picture'], [app.hideAllSubWindows, attach_pic])
    app.stopSubWindow()

    app.go()


get_gui()
