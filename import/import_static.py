import psycopg2
import sqlite3

import sys

def import_jumps(dbs, db):
    cur = db.cursor()
    curs = dbs.cursor()
    curs.execute('SELECT fromRegionID,fromConstellationID,fromSolarSystemID,toSolarSystemID,toConstellationID,toRegionID FROM mapSolarSystemJumps')
    for row in curs:
        print row[2],"to",row[3]
        cur.execute('SELECT fromsystem FROM jumps WHERE fromsystem = %s AND tosystem = %s', (row[2], row[3]))
        r = cur.fetchone()
        if not r:
            cur.execute('INSERT INTO jumps (fromregion, fromconstellation, fromsystem, tosystem, toconstellation, toregion) VALUES (%s,%s,%s,%s,%s,%s)',
                        (row[0], row[1], row[2], row[3], row[4], row[5]))
            print "INSERT"
        db.commit()
        

def import_regions(dbs,db):
    cur = db.cursor()
    curs = dbs.cursor()
    curs.execute('SELECT regionID,regionName FROM mapRegions')
    for row in curs:
        print row[0],'=',row[1]
        cur.execute('SELECT regionid FROM regions WHERE regionid = %s', (row[0],))
        r = cur.fetchone()
        if r:
            cur.execute('UPDATE regions SET regionname = %s WHERE regionid = %s', (row[1], row[0]))
        else:
            cur.execute('INSERT INTO regions (regionid, regionname) VALUES (%s, %s)', (row[0], row[1]))
            print "INSERT"
        db.commit()


def import_systems(dbs,db):
    cur = db.cursor()
    curs = dbs.cursor()
    curs.execute('SELECT solarSystemID,solarSystemName,regionID,constellationID,security,factionID FROM mapSolarSystems')
    for row in curs:
        faction = row[5]
        if not faction:
            faction = 0
        print row[0],'=',row[1], " faction ", faction
        cur.execute('SELECT systemid FROM systems WHERE systemid = %s', (row[0],))
        r = cur.fetchone()
        if r:
            cur.execute('UPDATE systems SET systemname = %s, security = %s, truesec = %s, constellationid = %s, faction = %s WHERE systemid = %s', (row[1], row[4], row[4], row[3], faction, row[0]))
        else:
            cur.execute('INSERT INTO systems (systemid, systemname, regionid, faction, security, constellationid, truesec) VALUES (%s, %s, %s, %s, %s, %s, %s)', (row[0], row[1], row[2], faction, row[4], row[3], row[4]))
            print "INSERT"
        db.commit()

def import_stations(dbs,db):
    cur = db.cursor()
    curs = dbs.cursor()
    curs.execute('SELECT stationID, stationName, solarSystemID from staStations')
    for row in curs:
        print row[0],'=',row[1]
        cur.execute('SELECT stationname FROM stations WHERE stationid = %s', (row[0],))
        r = cur.fetchone()
        if r:
            cur.execute('UPDATE stations SET stationname = %s, systemid = %s WHERE stationid = %s', (row[1], row[2], row[0]))
        else:
            cur.execute('INSERT INTO stations (stationid, stationname, systemid) VALUES (%s, %s, %s)', (row[0], row[1], row[2]))
            print "INSERT"
        db.commit()

def main(sqle):
    db = psycopg2.connect(database = 'evec', user = 'evec')
    dbs = sqlite3.connect(sqle)
    import_jumps(dbs, db)
    import_regions(dbs, db)
    import_systems(dbs, db)
    import_stations(dbs, db)


if __name__ == "__main__":
    main(sys.argv[1])
    

