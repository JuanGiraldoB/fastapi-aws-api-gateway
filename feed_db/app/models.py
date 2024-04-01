from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Circuit(Base):
    __tablename__ = 'circuit'
    circuit_id = Column(Integer, primary_key=True)
    name = Column(String)
    # one circuit can have many races
    races = relationship('Race', backref='circuit')


class Team(Base):
    __tablename__ = 'team'
    team_id = Column(Integer, primary_key=True)
    name = Column(String)
    points = Column(Integer)
    position = Column(Integer)
    # one team can have many drivers
    drivers = relationship('Driver', backref='team')


class Driver(Base):
    __tablename__ = 'driver'
    driver_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    name = Column(String)
    nationality = Column(String)
    points = Column(Integer)
    position = Column(Integer)
    # one driver can have many results
    results = relationship('RaceResult', backref='driver')
    # one driver can have many fastest laps
    fastest_laps = relationship('FastestLap', backref='driver')


class Race(Base):
    __tablename__ = 'race'
    race_id = Column(Integer, primary_key=True)
    circuit_id = Column(Integer, ForeignKey('circuit.circuit_id'))
    fastest_lap_id = Column(Integer, ForeignKey('fastest_lap.fastest_lap_id'))
    winner = Column(String)
    year = Column(Integer)
    date = Column(String)
    # one race can have many results
    results = relationship('RaceResult', backref='race')


class RaceResult(Base):
    __tablename__ = 'race_result'
    result_id = Column(Integer, primary_key=True)
    position = Column(Integer)
    driver_id = Column(Integer, ForeignKey('driver.driver_id'))
    race_id = Column(Integer, ForeignKey('race.race_id'))
    fastest_lap_id = Column(Integer, ForeignKey('fastest_lap.fastest_lap_id'))


class FastestLap(Base):
    __tablename__ = 'fastest_lap'
    fastest_lap_id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('driver.driver_id'))
    race_id = Column(Integer, ForeignKey('race.race_id'))
    # lap time can be a string to accommodate different time formats
    time = Column(String)
